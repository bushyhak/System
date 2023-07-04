from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("contact/", views.contact, name="contact"),
    path("book/", views.book, name="book"),
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
    path("dashboard/settings/", views.settings, name="dashboard_settings"),
    path("dashboard/report/", views.report, name="dashboard_report"),
    ##########################################################################
    path("register/", views.register, name="register"),
    path("edit/", views.edit, name="edit"),
    path("booking/", views.booking_view, name="booking"),
    path("reschedule/<int:appointment_id>/", views.reschedule_view, name="reschedule"),
    path("cancel/<int:appointment_id>/", views.cancel_appointment, name="cancel"),
]
