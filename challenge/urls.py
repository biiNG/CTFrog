from django.urls import path
from . import views

urlpatterns = [
    path('', views.ChallengeHome, name='challenge-home'),
    path('<int:primarykey>/', views.ChallengeDetail, name='challenge-detail'),
    path("CheckFlag/<int:primarykey>/", views.CheckFlag, name='check-flag'),
    # path('<int:pk>/result/', views.challengeresult),
]
