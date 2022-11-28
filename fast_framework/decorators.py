from enum import Enum
import functools
import inspect

from fastapi import params
from fastapi.datastructures import Default, DefaultPlaceholder
from fastapi.encoders import DictIntStrAny, SetIntStr
from fastapi.utils import generate_unique_id

from starlette.responses import JSONResponse, Response
from starlette.routing import BaseRoute
from starlette.routing import Mount as Mount  # noqa

from fastapi.routing import APIRoute
from typing import Any, Callable, Dict, List, Optional, Union, TypeVar, Sequence, Type, Awaitable
from typing_extensions import ParamSpec

P = ParamSpec("P")
R = TypeVar("R")
T = TypeVar("T")


def compatible_method(func: Callable[P, R]) -> Callable[P, R]:
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        return func(*args, **kwargs)

    @functools.wraps(func)
    async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> Awaitable[Callable[P, R]]:
        return await func(*args, **kwargs)

    return async_wrapper if inspect.iscoroutinefunction(func) else wrapper

def actions(
    methods: List[str],
    path: str,
    *,
    response_model: Any = None,
    status_code: Optional[int] = None,
    tags: Optional[List[Union[str, Enum]]] = None,
    dependencies: Optional[Sequence[params.Depends]] = None,
    summary: Optional[str] = None,
    description: Optional[str] = None,
    response_description: str = "Successful Response",
    responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
    deprecated: Optional[bool] = None,
    operation_id: Optional[str] = None,
    response_model_include: Optional[Union[SetIntStr, DictIntStrAny]] = None,
    response_model_exclude: Optional[Union[SetIntStr, DictIntStrAny]] = None,
    response_model_by_alias: bool = True,
    response_model_exclude_unset: bool = False,
    response_model_exclude_defaults: bool = False,
    response_model_exclude_none: bool = False,
    include_in_schema: bool = True,
    response_class: Union[Type[Response], DefaultPlaceholder] = Default(JSONResponse),
    route_class_override: Optional[Type[APIRoute]] = None,
    callbacks: Optional[List[BaseRoute]] = None,
    openapi_extra: Optional[Dict[str, Any]] = None,
    generate_unique_id_function: Union[
        Callable[[APIRoute], str], DefaultPlaceholder
    ] = Default(generate_unique_id),
) -> Callable[[T], T]:
    methods = ['get'] if (methods is None) else methods
    methods = [method.lower() for method in methods]
    class Action():
        def __init__(self, func: Callable[..., Any]) -> None:
            self.func: Callable[..., Any] = func

        def __set_name__(self, owner: T, name: str) -> None:
            setattr(owner, name, compatible_method(self.func))

            _actions = getattr(owner, '_actions')
            _actions[self.func.__name__] = dict(
                    methods=methods,
                    path=path,
                    response_model=response_model,
                    status_code=status_code,
                    tags=tags,
                    dependencies=dependencies,
                    summary=summary,
                    description=description,
                    response_description=response_description,
                    responses=responses,
                    deprecated=deprecated,
                    operation_id=operation_id,
                    response_model_include=response_model_include,
                    response_model_exclude=response_model_exclude,
                    response_model_by_alias=response_model_by_alias,
                    response_model_exclude_unset=response_model_exclude_unset,
                    response_model_exclude_defaults=response_model_exclude_defaults,
                    response_model_exclude_none=response_model_exclude_none,
                    include_in_schema=include_in_schema,
                    response_class=response_class,
                    name=name,
                    route_class_override=route_class_override,
                    callbacks=callbacks,
                    openapi_extra=openapi_extra,
                    generate_unique_id_function=generate_unique_id_function,
                )

            setattr(owner, '_actions', _actions)

    return Action
