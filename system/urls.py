from django.urls import path
from . import views


urlpatterns = [ 
    path('', views.home),
    path('contact/', views.contact),
    path('book/', views.appointment),
    path('schedule', views.schedule)
]