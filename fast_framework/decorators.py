from enum import Enum
from typing import List, Dict, Any, Callable, Optional, Union
import functools
from enum import Enum
from typing import (
    Any,
    Callable,
    Coroutine,
    Dict,
    List,
    Optional,
    Sequence,
    Set,
    Tuple,
    Type,
    Union,
)

from fastapi import params
from fastapi.datastructures import Default, DefaultPlaceholder

from fastapi.encoders import DictIntStrAny, SetIntStr
from fastapi.utils import (
    generate_unique_id,
)
from pydantic import BaseModel
from pydantic.error_wrappers import ErrorWrapper, ValidationError
from pydantic.fields import ModelField, Undefined
from starlette import routing
from starlette.concurrency import run_in_threadpool
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import BaseRoute, Match
from starlette.routing import Mount as Mount  # noqa
from starlette.routing import (
    compile_path,
    get_name,
    request_response,
    websocket_session,
)

from fastapi.routing import APIRoute


def compatible_method(func: Callable[[Any], None]):
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        return func(*args, **kwargs)

    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs) -> Any:
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
    name: Optional[str] = None,
    route_class_override: Optional[Type[APIRoute]] = None,
    callbacks: Optional[List[BaseRoute]] = None,
    openapi_extra: Optional[Dict[str, Any]] = None,
    generate_unique_id_function: Union[
        Callable[[APIRoute], str], DefaultPlaceholder
    ] = Default(generate_unique_id),
):
    """ """
    rename = name
    class Action:
        def __init__(self, func: Callable[[Any], None]) -> None:
            self.func: Callable[[Any], None] = func

        def __set_name__(self, owner, name):
            setattr(owner, name, compatible_method(self.func))

            _actions = getattr(owner, '_actions')
            _actions[self.func.__name__] = {
                'path': path,
                'methods': methods,
                'schema_in_annotation': dict(
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
                    name=rename,
                    route_class_override=route_class_override,
                    callbacks=callbacks,
                    openapi_extra=openapi_extra,
                    generate_unique_id_function=generate_unique_id_function,
                ),
            }
            setattr(owner, '_actions', _actions)


    return Action
