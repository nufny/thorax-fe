from django.urls import path

from . import views

urlpatterns = [
    path("/", views.allow, name="allow"),
]
