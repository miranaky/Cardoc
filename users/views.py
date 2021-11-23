import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.models import User
from users.serializers import UserSerializer


class UserCreateView(CreateModelMixin, GenericAPIView):
    """Sign up view"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = self.perform_create(serializer)
            print(user.pk)
            headers = self.get_success_headers(serializer.data)
            encoded_jwt = jwt.encode(
                {"pk": user.pk}, settings.SECRET_KEY, algorithm="HS256"
            )
            return Response(
                {"access_token": encoded_jwt},
                status=status.HTTP_200_OK,
                headers=headers,
            )
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        return serializer.save()


@api_view(["POST"])
def login(request):
    """Login view"""

    username = request.data.get("username")
    password = request.data.get("password")
    if not all([username, password]):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if user:
        encoded_jwt = jwt.encode(
            {"pk": user.pk},
            settings.SECRET_KEY,
            algorithm="HS256",
        )
        return Response(data={"access_token": encoded_jwt})
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
