import datetime
from dateutil.rrule import rrule, DAILY
from collections import OrderedDict
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from django.db.models import Count
from django.db.models.functions import TruncDay

from ..serializers import PageURLSerializer
from ..models import PageURL, Visit


class CountryAPIView(APIView):
    authentication_classes = (IsAuthenticated, )

    def get(self, request, format=None):
        pages = PageURL.objects.filter(
            author=self.request.user
        ).values_list('pk', flat=True)
        res = {}
        if pages.exist():
            visits = Visit.objects.filter(
                url_id__in=pages
            ).exclude(country_code__isnull=True).values('country_code').annotate(total=Count('country_code'))
            for i in visits.values('total', 'country_code'):
                res[i['country_code'].lower()] = str(i['total'])

        return Response(res)


class DeviceAPIView(APIView):
    authentication_classes = (IsAuthenticated, )

    def get(self, request, format=None):
        pages = PageURL.objects.filter(
            author=self.request.user
        ).values_list('pk', flat=True)
        visits = Visit.objects.filter(
            url_id__in=pages
        )
        mobile = visits.filter(is_mobile=True).count()
        pc = visits.filter(is_pc=True).count()
        res = {
            'pc': pc,
            'mobile': mobile
        }

        return Response(res)


class DailyHitsAPIView(APIView):
    authentication_classes = (IsAuthenticated, )

    def get(self, request, format=None):
        startdate = datetime.date.today()
        enddate = startdate - datetime.timedelta(days=7)
        pages = PageURL.objects.filter(
            author=self.request.user,
        ).values_list('pk', flat=True)
        q = Visit.objects.filter(
            url_id__in=pages,
            date__range=[enddate, startdate]
        ).annotate(day=TruncDay('date')).values('day').annotate(count=Count('day')).values('day', 'count')
        es = {i['day'].strftime("%Y,%-m,%d"): i['count'] for i in q}

        for dt in rrule(DAILY, dtstart=startdate, until=enddate):
            if not es.get(dt.strftime("%Y,%-m,%d")):
                es[dt.strftime("%Y,%-m,%d")] = 0
        d = OrderedDict(sorted(es.items(), key=lambda t: t[0]))
        return Response(d)


class BestPerformersAPIView(ListAPIView):
    authentication_classes = (IsAuthenticated, )
    serializer_class = PageURLSerializer

    def get_queryset(self):
        return PageURL.objects.filter(
            author=self.request.user,
        ).annotate(total=Count('hits')).order_by('-hits')[:5]
