import uuid
from django.contrib.auth import get_user_model
from rest_framework import authentication
from rest_framework import exceptions

from .models import Token

User = get_user_model()


class TokenAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        header = request.META.get('HTTP_TOKEN', 'jrfr')

        if header:
            apikey = header
        else:
            if request.method == 'GET':
                apikey = request.query_params.get('apikey')
            elif request.method == 'POST':
                apikey = request.data.get('apikey')
            else:
                return None

        try:
            print apikey
            token = Token.objects.get(uuid=apikey)
        except Token.DoesNotExist:
            raise exceptions.AuthenticationFailed('Token does not exist')

        return (token.user, None)

    def authenticate_header(self, request):
        return 'Not authenticated'
