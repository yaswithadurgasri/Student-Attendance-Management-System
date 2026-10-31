from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.home,
        name="dashboard_home"
    ),

    path(
        "add/<str:kind>/",
        views.add,
        name="dashboard_add"
    ),

    path(
        "edit/<str:kind>/<int:pk>/",
        views.edit,
        name="dashboard_edit"
    ),

    path(
        "delete/<str:kind>/<int:pk>/",
        views.delete,
        name="dashboard_delete"
    ),

]
