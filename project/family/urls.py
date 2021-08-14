from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token
from . import views

from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView
from django.conf.urls import url

# from rest_framework_swagger.views import get_swagger_view











# schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    path("register", views.register_person, name="register"),
    path("login", obtain_auth_token, name="login"),
    path("create-family", views.create_family, name="create-family"),
    path("package-selection", views.select_package, name="package-selection"),
    path("package-change", views.select_package, name="package-change"),
    path("package-delete", views.delete_package, name="package-delete"),
]



