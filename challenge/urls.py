from django.urls import path
from . import views

urlpatterns = [
    path('', views.ChallengeHome),
    # path('<int:pk>/', views.challengedetail),
    # path('<int:pk>/result/', views.challengeresult),
]
