from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [ 
    path('', views.home),
    path('contact/', views.contact,name='contact'),
    path('book/', views.book, name='book'),
    path('about/', views.about, name='about'),
    # path('login/', views.user_login, name = 'login'),
    path('register/',views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),


]