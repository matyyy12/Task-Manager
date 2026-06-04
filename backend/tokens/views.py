from django.contrib.auth.hashers import check_password
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from user.models import User
from rest_framework.views import APIView

from .authentication import BearerAuthentication
from .models import Token


# Create your views here.


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = User.objects.filter(username=username).first()
        if user is None:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if not check_password(password, user.password):
            return Response({'message': 'Wrong password'}, status=status.HTTP_401_UNAUTHORIZED)

        token = Token.objects.filter(user=user).first() or Token(user=user)
        token.access_token = Token.generate_key()
        token.refresh_token = Token.generate_key()
        token.access_expires_at = Token.get_access_expiry()
        token.refresh_expires_at = Token.get_refresh_expiry()
        token.save()

        return Response({'access_token': token.access_token,
                              'refresh_token': token.refresh_token}, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class RefreshView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh_token')

        token = Token.objects.filter(refresh_token=refresh_token).first()

        if token is None:
            return Response({'message': 'Token not found'}, status=status.HTTP_404_NOT_FOUND)

        if token.is_refresh_expired():
            return Response({'message': 'Refresh token expired, please log in again'}, status=status.HTTP_401_UNAUTHORIZED)

        token.access_token = Token.generate_key()
        token.access_expires_at = Token.get_access_expiry()
        token.save()

        return Response({'access_token': token.access_token}, status=status.HTTP_200_OK)


class LogoutView(APIView):
    authentication_classes = [BearerAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.auth.delete()
        return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
