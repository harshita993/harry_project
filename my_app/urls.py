from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('home/',views.index,name="home"),
    path('about/',views.about,name="about"),
    path('contact/',views.contact,name="contact"),
    path('service/',views.service,name="service"),
    path('',views.login_view,name="login"),
    path('logout/',views.logoutuser,name="logout"),
]