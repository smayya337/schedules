from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    accepted_terms = models.BooleanField(default=False)
    graduation_year = models.PositiveSmallIntegerField(null=True)
    is_student = models.BooleanField(default=False)

    nickname = models.CharField(max_length=30, blank=True)

    publish_data = models.BooleanField(
        default=False,
        verbose_name="Publish my data",
        help_text="Unless this is set, your data will not appear publicly.",
    )

    last_modified = models.DateTimeField(auto_now=True)

    @property
    def preferred_name(self):
        return self.nickname if self.nickname else self.first_name

    def __str__(self):
        return f"{self.preferred_name} {self.last_name}"
