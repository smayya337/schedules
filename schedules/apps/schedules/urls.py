from django.urls import path

from . import views

app_name = "destinations"

urlpatterns = [
    path("", views.StudentPeriodListView.as_view(), name="students"),
]
