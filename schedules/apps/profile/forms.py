from typing import Any, Dict

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from django import forms
from django.contrib import messages

from schedules.apps.authentication.models import User
from schedules.apps.schedules.models import Period


class ProfilePublishForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"

        self.helper.add_input(Submit("submit", "Submit"))

    class Meta:
        model = User
        fields = ["publish_data", "graduation_year"]


class PeriodForm(forms.ModelForm):
    class Meta:
        model = Period
        fields = ["number", "teacher"]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        self.is_edit = kwargs.pop("edit", False)
        super().__init__(*args, **kwargs)

    def clean(self) -> Dict[str, Any]:
        cleaned_data = super().clean()

        # Ensure that the college is not a duplicate for this user
        # Yes, this is weird. Basically: if we are not editing
        # (i.e. creating a new one), we make sure that
        # the user does not have a Decision object with that college already.
        # If we are editing, then we ensure that the college
        # has not changed. If it has changed, then we
        # make sure that the user does not have a Decision object with that college already.
        if (
            not self.is_edit
            and Period.objects.filter(
                user=self.request.user, number=cleaned_data.get("number")
            ).count()
            > 0
        ) or (
            self.is_edit
            and Period.objects.filter(
                user=self.request.user,
                id=self.instance.id,
                number=cleaned_data.get("number"),
            ).count()
            != 1
            and Period.objects.filter(
                user=self.request.user, number=cleaned_data.get("number")
            ).count()
            > 0
        ):
            self.add_error("period", "You cannot have two classes during the same period!")

        return cleaned_data

    def save(self, commit: bool = True) -> Any:
        super().save(commit=commit)
