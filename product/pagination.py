from rest_framework.pagination import PageNumberPagination


class ProductPagination(PageNumberPagination):
    page_size = 1
    page_query_param = 'record'
    page_size_query_param = 'size'
    max_page_size = 10