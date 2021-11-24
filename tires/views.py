import requests
from rest_framework import status
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from tires.models import TiresInfo
from tires.serializers import TiresInfoCreateSerializer
from users.models import User


def tire_size(size: str) -> tuple:
    if "/" in set(size) and "R" in set(size):
        width, remain = size.split("/")
        profile, rim = remain.split("R")
        return width, profile, rim
    return None, None, None


def remove_objs(objs):
    for obj in objs:
        obj.delete()


class CreateTiresInfoView(CreateModelMixin, GenericAPIView):
    queryset = TiresInfo.objects.all()
    serializer_class = TiresInfoCreateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if len(request.data) > 5:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # check username exist.
        for info in request.data:
            try:
                User.objects.get(username=info.get("id"))
            except User.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        objs = []
        for info in request.data:
            try:
                objs.append(self.create(info, *args, **kwargs))
            except AttributeError or ValidationError:
                remove_objs(objs)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            except APIException:
                remove_objs(objs)
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        user = User.objects.get(username=request.get("id")).id
        request["username"] = user
        request["trim_id"] = request.pop("trimId")
        serializer = self.get_serializer(data=request)
        serializer.is_valid(raise_exception=True)
        return self.perform_create(serializer)

    def perform_create(self, serializer):
        url = f"https://dev.mycar.cardoc.co.kr/v1/trim/{serializer.validated_data.get('trim_id')}"

        driving_data = requests.get(url, timeout=1).json().get("spec").get("driving")

        #  Tires value validate
        front_tires = driving_data.get("frontTire").get("value")
        front_width, front_profile, front_rim = tire_size(front_tires)
        rear_tires = driving_data.get("rearTire").get("value")
        rear_width, rear_profile, rear_rim = tire_size(rear_tires)
        if None in (
            front_width,
            front_profile,
            front_rim,
            rear_width,
            rear_profile,
            rear_rim,
        ):
            raise APIException()

        return serializer.save(
            front_width=front_width,
            front_profile=front_profile,
            front_rim=front_rim,
            rear_width=rear_width,
            rear_profile=rear_profile,
            rear_rim=rear_rim,
        )
