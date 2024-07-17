from rest_framework import pagination


class TechStackCursorPagination(pagination.CursorPagination):
    page_size = 10
    ordering = '-created_at'
