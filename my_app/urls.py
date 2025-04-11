from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('home/',views.index,name="home"),
    path('about/',views.about,name="about"),
    path('contact/',views.contact,name="contact"),
    path('add/', views.add_icecream, name='add_icecream'),
    path('icecream/<int:id>/', views.icecream_detail, name='icecream_detail'),
    path('icecream/<int:id>/edit/', views.icecream_edit, name='icecream_edit'),
    path('icecream/<int:id>/delete/', views.icecream_delete, name='icecream_delete'),
    path('service/',views.service,name="service"),
    path('',views.login_view,name="login"),
    path('register/', views.register_view, name='register'),
    path('update_contact/<int:id>/',views.update_contact,name="update_contact"),
    path('delete_contact/<int:id>/',views.delete_contact,name="delete_contact"),
    path('logout/',views.logoutuser,name="logout"),
]