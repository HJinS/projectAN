from tkinter.tix import INTEGER
from rest_framework.pagination import CursorPagination


class Paginator(CursorPagination):
    page_size = 30
    ordering = 'id'
    
class LikePaginator(CursorPagination):
    page_size = 30
    ordering = 'id'