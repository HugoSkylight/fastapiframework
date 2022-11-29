from typing import Dict, Any
from pydantic import BaseSettings
import functools


class FastSettings(BaseSettings):

    ORM_BACKENDS: Dict[str, Any] = {
        'default': {}
    }


@functools.lru_cache()
def get_fast_settings() -> FastSettings:
    return FastSettings()