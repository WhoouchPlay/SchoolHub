from django.urls import path

from . import views


urlpatterns = [
    path("", views.schedule_view, name="schedule_view"),
    path("filtered/", views.schedule_view_filtered, name="schedule_view_filtered"),
    path("add/", views.add_schedule, name="add_schedule"),
    path("edit/<int:id>/", views.edit_schedule, name="edit_schedule"),
    path("remove/<int:id>/", views.remove_schedule, name="remove_schedule"),
]