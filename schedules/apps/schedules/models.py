from django.db import models
from django.conf import settings


class Teacher(models.Model):
    """Represents a teacher."""

    name = models.CharField(max_length=250, null=False, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


PERIOD_NUMBERS = [(x, x) for x in settings.PERIODS]

class Period(models.Model):
    """Represents a period for a student."""

    number = models.IntegerField(choices=PERIOD_NUMBERS)
    user = models.ForeignKey("authentication.User", on_delete=models.CASCADE)
    teacher = models.ForeignKey("schedules.Teacher", on_delete=models.CASCADE)

    class Meta:
        ordering = ["number"]
