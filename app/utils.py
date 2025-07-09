import inspect
from functools import wraps

from fastapi import HTTPException


def lessthan_x(x: int, arg_name=None, message="Input is too short."):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            sig = inspect.signature(func)
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()

            if arg_name:
                value = bound.arguments.get(arg_name, "")
            else:
                value = next(iter(bound.arguments.values()), "")
            if len(value.strip()) < x:
                raise HTTPException(status_code=400, detail=message)
            return func(*args, **kwargs)

        return wrapper

    return decorator
