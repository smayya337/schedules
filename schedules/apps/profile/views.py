from typing import Any, Dict

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpRequest
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, UpdateView

from schedules.apps.authentication.decorators import require_accept_tos
from schedules.apps.schedules.models import Period

from .forms import PeriodForm, ProfilePublishForm


@login_required
@require_accept_tos
def profile_view(request: HttpRequest):
    # mypy is annoying.
    test_scores = TestScore.objects.filter(user=request.user)  # type: ignore
    periods = Period.objects.filter(user=request.user)  # type: ignore

    # A POST request would mean that the user is saving their profile publication status
    if request.method == "POST":
        profile_form = ProfilePublishForm(request.POST, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()

            messages.success(request, "Your preferences have been changed.")
    else:
        profile_form = ProfilePublishForm(instance=request.user)

    context = {
        "test_scores_list": test_scores,
        "periods_list": periods,
        "profile_form": profile_form,
    }

    return render(request, "profile/profile.html", context=context)


class PeriodCreateView(
    LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, CreateView
):
    model = Period
    form_class = PeriodForm
    template_name = "profile/period_form.html"
    success_message = "Period created successfully."

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self) -> Dict[str, Any]:
        form_kwargs = super().get_form_kwargs()
        form_kwargs["request"] = self.request
        return form_kwargs

    def test_func(self):
        assert self.request.user.is_authenticated
        return self.request.user.is_student and self.request.user.accepted_terms

    def get_success_url(self):
        return reverse("profile:index")


class PeriodUpdateView(
    LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, UpdateView
):
    model = Period
    form_class = PeriodForm
    template_name = "profile/period_form.html"
    success_message = "Period created successfully."

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self) -> Dict[str, Any]:
        form_kwargs = super().get_form_kwargs()
        form_kwargs["request"] = self.request
        form_kwargs["edit"] = True
        return form_kwargs

    def get_queryset(self):
        assert self.request.user.is_authenticated
        owner = self.request.user
        return self.model.objects.filter(user=owner)

    def test_func(self):
        assert self.request.user.is_authenticated
        return self.request.user.is_student and self.request.user.accepted_terms

    def get_success_url(self):
        return reverse("profile:index")


class PeriodDeleteView(
    LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, DeleteView
):
    model = Period
    template_name = "profile/period_delete.html"
    success_message = "Period deleted successfully."

    def get_queryset(self):
        assert self.request.user.is_authenticated
        owner = self.request.user
        return self.model.objects.filter(user=owner)

    def test_func(self):
        assert self.request.user.is_authenticated
        return self.request.user.is_student and self.request.user.accepted_terms

    def get_success_url(self):
        return reverse("profile:index")
