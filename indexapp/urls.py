from django.urls import path
from .views import (
    index, about, login_view, logout_view, signup_view, dashboard_view,
    projects_list, project_detail, contact_view
)

urlpatterns = [
    path("", index, name="index"),
    path("about/", about, name="about"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("signup/", signup_view, name="signup"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("projects/", projects_list, name="projects_list"),
    path("projects/<slug:slug>/", project_detail, name="project_detail"),
    path("contact/", contact_view, name="contact"),
]
