from django.urls import path
from . import views


urlpatterns = [ 
    path('', views.home),
    path('contact/', views.contact),
    path('book/', views.appointment),
    path('about/', views.schedule),
    path('login', views.login)

]