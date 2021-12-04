from django.contrib.auth import logout
from django.urls import path
from .views import register_view, login_view,profile_view,logout_view

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login_view'),
    path('profile/',profile_view,name = 'profile_view'),
    path('logout/',logout_view,name='logout_view'),

]
