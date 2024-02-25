from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import (
    UserRegisterationSerializer,
    CustomUserLoginSerializer,
    UserProfileSerializer,
    UserChangePasswordSerializer,
    UserChangePasswordEmailSerializer,
)
from django.contrib.auth import authenticate
from Auth.renderers import CustomUserRenders
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


# generating token manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


# Create your views here.


class Root(APIView):
    renderer_classes = []

    def list(self, request, format=None):
        return Response({"message": "hello"}, status=status.HTTP_200_OK)


class UserRegisteration(APIView):
    renderer_classes = [CustomUserRenders]

    def post(self, request, format=None):
        serializer = UserRegisterationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response(
                {"token": token, "msg": "Registeration success"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    renderer_classes = [CustomUserRenders]

    def post(self, request, format=None):
        serializer = CustomUserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get("email")
            password = serializer.data.get("password")
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response(
                    {"token": token, "msg": "login was successful"},
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    {"msg": "Email or Password is not valid"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    renderer_classes = [CustomUserRenders]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChangeUserPassword(APIView):
    renderer_classes = [CustomUserRenders]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(
            data=request.data, context={"user": request.user}
        )
        if serializer.is_valid(raise_exception=True):
            return Response(
                {"msg": "Password is successfully changed"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserChangePasswordEmailView(APIView):
    renderer_classes = [CustomUserRenders]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = UserChangePasswordEmailSerializer(data=request.data)
        if serializer.is_valid():
            return Response(
                {"msg": "Password reset link send. Please check your Email"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class UserPasswordRestView(APIView):
#    renderer_classes=[CustomUserRenders]
#    def post(self, request,uid,token,format=None):
#       serializer=UserPasswordResetSerializer(data=request.data,context={
#          'uid':uid,
#          'token':token
#       })
#       if serializer.is_valid():
#          return Response({'msg':'Password is changed successfully'},status=status.HTTP_200_OK)
#       return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
