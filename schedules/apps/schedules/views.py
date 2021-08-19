from typing import Optional

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Q, QuerySet
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from ..authentication.models import User
from .models import Teacher, Period


class StudentPeriodListView(
    LoginRequiredMixin, UserPassesTestMixin, ListView
):  # pylint: disable=too-many-ancestors
    model = User
    paginate_by = 20

    def get_queryset(self):
        # Superusers can use the "all" GET parameter to see all data
        if self.request.GET.get("all", None) is not None:
            if self.request.user.is_superuser and self.request.user.is_staff:
                queryset = User.objects.all()
            else:
                raise PermissionDenied()
        else:
            queryset = User.objects.filter(publish_data=True)

        queryset = queryset.filter(is_senior=True).order_by("last_name", "first_name")

        teacher_id: Optional[str] = self.request.GET.get("teacher", None)
        if teacher_id is not None:
            if not teacher_id.isdigit():
                raise Http404()

            get_object_or_404(Teacher, id=teacher_id)
            queryset = queryset.filter(period__teacher__id=teacher_id)

        search_query = self.request.GET.get("q", None)
        if search_query is not None:
            queryset = queryset.filter(
                Q(first_name__icontains=search_query)
                | Q(last_name__icontains=search_query)
                | Q(nickname__icontains=search_query)
                | Q(biography__icontains=search_query)
            )

        return queryset

    def get_context_data(
        self, *, object_list=None, **kwargs
    ):  # pylint: disable=unused-argument
        context = super().get_context_data(**kwargs)

        teacher_id: Optional[str] = self.request.GET.get("teacher", None)
        if teacher_id is not None:
            context["teacher"] = get_object_or_404(Teacher, id=teacher_id)

        search_query = self.request.GET.get("q", None)
        if search_query is not None:
            context["search_query"] = search_query

        return context

    def test_func(self):
        assert self.request.user.is_authenticated
        return self.request.user.accepted_terms

    template_name = "schedules/student_list.html"


# class TeacherDestinationListView(
#     LoginRequiredMixin, UserPassesTestMixin, ListView
# ):  # pylint: disable=too-many-ancestors
#     model = Teacher
#     paginate_by = 20
#
#     def get_queryset(self) -> QuerySet:
#         search_query = self.request.GET.get("q", None)
#         if search_query is not None:
#             queryset = Teacher.objects.filter(
#                 Q(name__icontains=search_query)
#                 | Q(location__icontains=search_query)
#                 | Q(ceeb_code__icontains=search_query)
#             )
#         else:
#             queryset = Teacher.objects.all()
#
#         queryset = (
#             queryset.annotate(  # type: ignore  # mypy is annoying
#                 count_periods=Count(
#                     "period", filter=Q(period__user__publish_data=True)
#                 ),
#             )
#             .filter(count_periods__gte=1)
#             .order_by("name")
#         )
#
#         return queryset
#
#     def get_context_data(
#         self, *, object_list=None, **kwargs
#     ):  # pylint: disable=unused-argument
#         context = super().get_context_data(**kwargs)
#
#         search_query = self.request.GET.get("q", None)
#         if search_query is not None:
#             context["search_query"] = search_query
#
#         return context
#
#     def test_func(self):
#         assert self.request.user.is_authenticated
#         return self.request.user.accepted_terms
#
#     template_name = "schedules/teacher_list.html"
