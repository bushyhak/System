from django.urls import path
from . import views


urlpatterns = [ 
    path('', views.home),
    path('contact/', views.contact,name='contact'),
    path('book/', views.book, name='book'),
    path('about/', views.about, name='about'),
    path('login/', views.user_login, name = 'login'),
    path('register/',views.register, name='register'),


]