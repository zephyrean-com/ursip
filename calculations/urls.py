from django.urls import path

from calculations.views import (
    StartPage,
    StatsAPIView,
    StatsView,
)

urlpatterns = [
    path('', StartPage.as_view(), name='start_page'),
    path('html/', StatsView.as_view(), name='html_demo'),
    path('json/', StatsAPIView.as_view(), name='json_demo'),
]
