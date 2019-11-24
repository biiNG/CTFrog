from django.urls import path
from . import views

urlpatterns = [
    path('', views.RankView.as_view(), name='index'),
]
