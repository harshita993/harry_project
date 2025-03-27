from django.contrib import admin
from django.urls import path
from my_app import views
urlpatterns = [
    path('',views.index,name="home"),
    path('about/',views.about,name="about"),
    path('contact/',views.contact,name="contact"),
    path('service/',views.service,name="service"),
]