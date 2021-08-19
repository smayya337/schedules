from django.contrib import admin

from .models import Teacher, Period


class TeacherAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name"]


class PeriodAdmin(admin.ModelAdmin):
    list_display = [
        "number",
        "user",
        "teacher"
    ]


admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Period, PeriodAdmin)
