from django.urls import path
from . import views

urlpatterns = [
    path('', views.ChallengeHome),
    path('<int:primarykey>/', views.ChallengeDetail),
    # path('<int:pk>/result/', views.challengeresult),
]
