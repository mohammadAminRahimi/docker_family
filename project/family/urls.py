from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path("register", views.register_person, name="register"),
    path("login", obtain_auth_token, name="login"),
    path("create-family", views.create_family, name="create-family"),
    path("package-selection", views.select_package, name="package-selection"),
    path("package-change", views.select_package, name="package-change"),
    path("package-delete", views.delete_package, name="package-delete"),
]



