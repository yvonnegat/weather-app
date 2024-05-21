# weather/urls.py
from django.urls import path
from . import views
urlpatterns = [
    path('getweather/', views.get_weather, name='get_weather'),
    path('', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
]
