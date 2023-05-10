import datetime
from typing import Any

from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView

from calculations import selectors


class StartPage(View):
    @staticmethod
    def get(request):
        return render(request, 'calculations/start_page.html')


class StatsView(View):
    @staticmethod
    def get(request):
        return HttpResponse(selectors.get_quantity_df().to_html())


class StatsAPIView(APIView):
    @staticmethod
    def get(request):
        def _date_keys_to_iso(dct: dict[datetime.date, Any]) -> dict[str, Any]:
            return {
                date.isoformat(): value
                for date, value in dct.items()
            }
        return Response(_date_keys_to_iso(selectors.get_quantity_dict()))
