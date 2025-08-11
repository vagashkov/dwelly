from rest_framework.pagination import PageNumberPagination


class BasePaginator(PageNumberPagination):
    """
    Base pagination management class
    """

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100
