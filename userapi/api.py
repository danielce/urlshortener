from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from shortener.models import PageURL, SimpleRedirection
from .serializers import PageURLSerializer, PageURLCreateSerializer, CampaignSerializer
from .authentication import TokenAuthentication


class PageURLListAPIView(ListAPIView):
    serializer_class = PageURLSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        user = self.request.user
        qs = PageURL.objects.filter(
            author=user, url_type=PageURL.SIMPLE)
        return qs


class PageURLCreateAPIView(CreateAPIView):
    serializer_class = PageURLSerializer
    authentication_classes = (TokenAuthentication,)

    def perform_create(self, serializer):
        campaign = self.request.data.get('campaign')
        long_url = self.request.data.get('long_url')
        author = self.request.user
        serializer.save(long_url=long_url, author=author,
            campaign=campaign)


class PageURLDetailAPIView(RetrieveAPIView):
    serializer_class = PageURLSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    pk_url_kwarg = 'url_id'
    pk_lookup_kwarg = 'url_id'
    lookup_field = 'url_id'
    queryset = PageURL.objects.all()


class SimpleRedirectionExpandAPIView(RetrieveAPIView):
    serializer_class = PageURLSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_object(self):
        longurl = self.kwargs['url_id']
        # s = SimpleRedirection.objects.filter(
        #     long_url=longurl
        # )[0].pageurl
        q = PageURL.objects.filter(
            simple__long_url=longurl,
            author=self.request.user,
            url_type=PageURL.SIMPLE
        )
        return q[0]


class CampaignCreateView(CreateAPIView):
    serializer_class = CampaignSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        author = self.request.user
        print serializer.save(owner=author)
