from typing import Any, List, Optional, Tuple, Dict
from fastapi import APIRouter


class BaseResource:
    def __init__(self) -> None:
        self.router_registry: List[Tuple[str, Any, Optional[List[str]]]] = []

    def register(self, *, prefix: str, router: APIRouter, tags: Optional[List[str]] = None) -> None:
        if tags is None:
            tags = self.get_default_tags(router=router)

        self.router_registry.append((prefix, router, tags))


    def get_endpoint(self) -> List[Any]:
        raise NotImplementedError("get_endpoint must be overridden")

    def get_default_tags(self, *, router: APIRouter) -> List[str]:
        """
        If `tags` is not specified, 
        attempt to automatically determine it from the viewset. 
        """
        raise NotImplementedError("get_default_tags must be overridden")


class GenericResource(BaseResource):

    def __init__(self, trailing_slash: bool=True) -> None:
        self.trailing_slash = '/' if trailing_slash else ''
        super().__init__()

    def get_default_tags(self, *, router: APIRouter) -> List[str]:
        model = getattr(router, 'model', None)

        assert model is not None, ('`tags` argument not specified, and could ' 
            'not automatically determine the name from the viewset, as ' 
            'it does not have a `.model` attribute.')

        return [model.__name__]

    def get_endpoint(self) -> List[Any]:
        endpoints = []
        for prefix, viewset, tags in self.router_registry:
            routes: List[Any] = self.get_routes(viewsets=viewset)

            for route in routes:
                actions: Dict[Any, Any] = self.get_actions(route)
                viewset.router.add
        return endpoints

    def get_routes(self, *, viewsets: Any) -> List[Any]:
        return []

    def get_actions(self, *, route: Any) -> Dict[Any, Any]:
        return {}