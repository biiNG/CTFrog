from django.urls import path
from .views import RankView

urlpatterns=[
    path('',RankView.as_view(),name='index'),
]