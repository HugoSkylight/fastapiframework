from fastapi import Request
from typing import Any
class BasePagination:
    
    def paginate_queryset(self, queryset: Any, request: Request):
        raise NotImplementedError("paginate_queryset must be implemented")

    def get_paginated_response(self, data: Any):
        raise NotImplementedError("get_paginated_response must be implemented")


class PageSizePagination(BasePagination):
    page_size = None
    page_query_param = "page"
    page_size_query_param = "page_size"
    max_page_size = 100

    def paginate_queryset(self, queryset: Any, request: Request):
        ...

    def get_page_number(self, request: Request):
        ...
    
    def get_paginated_response(self, data: Any):
        ...
    
    def get_page_size(self, request: Request):
        ...
