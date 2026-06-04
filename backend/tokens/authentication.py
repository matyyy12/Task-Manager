from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import Token

class BearerAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        access_token = auth_header.split(' ')[1]
        token = Token.objects.filter(access_token=access_token).first()

        if token is None or token.is_access_expired():
            raise AuthenticationFailed('Unauthorized')

        return token.user, token