from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("contact/", views.contact, name="contact"),
    path("about/", views.about, name="about"),
    ############################# Dashboard urls #############################
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/profile/", views.profile, name="dashboard_profile"),
    path("dashboard/child-info/", views.child_info, name="dashboard_child_info"),
    path("dashboard/child-info/add-child/", views.add_child, name="add_child"),
    path(
        "dashboard/child-info/child/<int:child_id>/",
        views.child_detail,
        name="child_detail",
    ),
    path(
        "dashboard/child-info/child/<int:child_id>/update/",
        views.update_child,
        name="update_child",
    ),
    path(
        "dashboard/child-info/child/<int:child_id>/delete/",
        views.delete_child,
        name="delete_child",
    ),
    path("dashboard/settings/", views.settings, name="dashboard_settings"),
    path("dashboard/report/", views.report, name="dashboard_report"),
    path("dashboard/appointments/", views.appointments, name="appointments"),
    path(
        "dashboard/appointments/new/", views.book_appointment, name="book_appointment"
    ),
    path(
        "dashboard/appointments/<int:id>/",
        views.appointment_detail,
        name="appointment_detail",
    ),
    path(
        "dashboard/appointments/<int:id>/reschedule/",
        views.reschedule_appointment,
        name="reschedule_appointment",
    ),
    path(
        "dashboard/appointments/<int:id>/cancel/",
        views.cancel_appointment,
        name="cancel_appointment",
    ),
    ##########################################################################
    path("register/", views.register, name="register"),
]
