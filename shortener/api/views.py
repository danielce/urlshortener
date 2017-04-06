from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated

from .authentication import TokenAuthentication
from .serializers import PageURLSerializer, PageURLCreateSerializer
from ..models import PageURL


class PageURLListAPIView(ListAPIView):
    serializer_class = PageURLSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        user = self.request.user
        qs = PageURL.objects.filter(author=user)
        return qs


class PageURLCreateAPIView(CreateAPIView):
    serializer_class = PageURLCreateSerializer
    authentication_classes = (TokenAuthentication,)