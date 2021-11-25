import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from tires.models import TiresInfo
from tires.serializers import TireInfoReadSerializer
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


class UserTiresInfoView(RetrieveAPIView):
    queryset = TiresInfo.objects.all()
    serializer_class = TireInfoReadSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = "username"
    lookup_field = "username"

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        page = self.paginate_queryset(instance)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(instance, many=True)
        return Response(serializer.data)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        assert lookup_url_kwarg in self.kwargs, (
            "Expected view %s to be called with a URL keyword argument "
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            "attribute on the view correctly."
            % (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        user = get_object_or_404(User, **filter_kwargs)
        obj = get_list_or_404(queryset, username=user.id)

        self.check_object_permissions(self.request, obj)
        return obj
