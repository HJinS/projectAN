from rest_framework.pagination import CursorPagination


class Paginator(CursorPagination):
    page_size = 30
    ordering = 'id'