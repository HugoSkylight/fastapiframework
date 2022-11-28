from typing import Any, List, Callable, Dict
from fastapi import APIRouter


class BaseResource:
    _actions: Dict[str, Dict[str, Any]] = {}

    def get_endpoint(self, name: str) -> Callable[..., Any]:
        raise NotImplementedError("get_endpoint must be overridden")

    def get_default_tags(self) -> List[str]:
        """
        If `tags` is not specified, 
        attempt to automatically determine it from the viewset. 
        """
        raise NotImplementedError("get_default_tags must be overridden")

    def as_router(self) -> APIRouter:
        raise NotImplementedError("as_router must be overridden")

class GenericResource(BaseResource):

    def __init__(self) -> None:
        self.router: APIRouter = APIRouter()

    def get_endpoint(self, name: str) -> Callable[..., Any]:
        return getattr(self, name)

    def get_default_tags(self) -> List[str]:
        return [self.__class__.__name__]

    def as_router(self):
        for name, annotations in self._actions.items():
            tags = getattr(self, "tags", self.get_default_tags())
            endpoint = self.get_endpoint(name)
            self.router.add_api_route(
                path=annotations["path"],
                endpoint=endpoint,
                methods=annotations["methods"],
                response_model=annotations["response_model"],
                status_code=annotations["status_code"],
                tags=tags,
                dependencies=annotations["dependencies"],
                summary=annotations["summary"],
                description=annotations["description"],
                response_description=annotations["response_description"],
                responses=annotations["responses"],
                deprecated=annotations["deprecated"],
                operation_id=annotations["operation_id"],
                response_model_include=annotations["response_model_include"],
                response_model_exclude=annotations["response_model_exclude"],
                response_model_by_alias=annotations["response_model_by_alias"],
                response_model_exclude_unset=annotations["response_model_exclude_unset"],
                response_model_exclude_defaults=annotations["response_model_exclude_defaults"],
                response_model_exclude_none=annotations["response_model_exclude_none"],
                include_in_schema=annotations["include_in_schema"],
                response_class=annotations["response_class"],
                name=annotations["name"],
                route_class_override=annotations["route_class_override"],
                callbacks=annotations["callbacks"],
            )
        return self.router