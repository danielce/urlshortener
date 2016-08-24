from django.contrib.auth import get_user_model
from rest_framework import authentication
from rest_framework import exceptions

from ..models import Token

User = get_user_model()


class TokenAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        header = request.META.get('HTTP_AUTHORIZATION')
        if header:
            token = header.split(" ")[1]
        else:
            if request.method == 'GET':
                token = request.query_params.get('apikey')
            elif request.method == 'POST':
                token = request.data.get('apikey')
            else:
                return None

        try:
            token = Token.objects.get(uuid=token)
        except Token.DoesNotExist:
            raise exceptions.AuthenticationFailed('Token does not exist')

        return (token.user, None)

    def authenticate_header(self, request):
        return 'Not authenticated'
