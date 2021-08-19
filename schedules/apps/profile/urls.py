from django.urls import path

from . import views

app_name = "profile"

urlpatterns = [
    path("", views.profile_view, name="index"),
    path("period/add", views.PeriodCreateView.as_view(), name="period_add"),
    path(
        "period/edit/<int:pk>",
        views.PeriodUpdateView.as_view(),
        name="period_edit",
    ),
    path(
        "period/delete/<int:pk>",
        views.PeriodDeleteView.as_view(),
        name="period_delete",
    ),
]
