import operator
from functools import reduce

from django.contrib import messages
from django.db.models import Q


class SearchableMixin:
    search_lookups = []
    query_param_name = "q"

    def get_queryset(self):
        query = self.request.GET.get("q", "")
        queryset = super().get_queryset()

        if query:
            queries_lookups = [Q(**{lookup: query}) for lookup in self.search_lookups]
            queries_lookups = reduce(operator.or_, queries_lookups)
            queryset = queryset.filter(queries_lookups)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["q"] = self.request.GET.get(self.query_param_name, "")
        return context


class PaginationMixin:
    paginate_by = 10

    def paginate_queryset(self, queryset, page_size):
        paginator, page, object_list, has_other_pages = super().paginate_queryset(queryset, page_size)
        page.adjusted_elided_pages = paginator.get_elided_page_range(page.number)

        return (paginator, page, object_list, has_other_pages)


class FormActionMixin:
    @property
    def success_message(self):
        return NotImplemented

    @property
    def error_message(self):
        return NotImplemented

    def form_valid(self, form):
        messages.info(self.request, self.success_message)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return super().form_invalid(form)
