from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [ 
    path('', views.home, name='home'),
    path('contact/', views.contact, name ='contact'),
    path('book/', views.book, name='book'),
    path('about/', views.about, name='about'),
    
#     # path('login/', views.user_login, name = 'login'),
#     path('register/',views.register, name='register'),

    path('login/', auth_views.LoginView.as_view(), name='login'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

#     # change password urls
    path('password-change/',
         auth_views.PasswordChangeView.as_view(), name='password_change'),

    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(),
         name='password_change_done'),     

#      #reset password urls
     path('password-reset/', auth_views.PasswordResetView.as_view(),
          name='password-reset'),

     path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(),
          name='password_reset_done'),

     path('password-reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),
          name='password_reset_confirm'),

     path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(),
          name='password_reset_complete'),

     path('', include('django.contrib.auth.urls')),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/',views.register, name='register'),
    path('edit/', views.edit, name='edit'),

#   add child url

    path('add-child/', views.add_child, name='add_child'),

# Booking url
    path('booking/',views.booking_view, name='booking'),
    path('reschedule/<int:appointment_id>/', views.reschedule_view, name='reschedule'),
    path('cancel/<int:appointment_id>/', views.cancel_appointment, name='cancel'),
    path('child/<int:child_id>/', views.child_detail, name='child_detail')
]

  



