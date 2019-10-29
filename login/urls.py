from django.urls import path
from . import views

app_name = 'user'
urlpatterns = [
    path('', views.login),
    path('login/', views.login, name='login'),
    path('index/', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
]
