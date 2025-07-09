import inspect
from functools import wraps

from fastapi import HTTPException


def lessthan_x(x: int, arg_name=None, message="Input is too short."):
    """
    Decorator factory to validate the minimum length of a string argument for FastAPI endpoints.

    Args:
        x (int): The minimum required length for the argument value after stripping whitespace.
        arg_name (str, optional): The name of the argument to check.
        If not provided, the first argument is used.
        message (str, optional): Custom error message to return if validation fails.

    Returns:
        function: A decorator that raises HTTPException(400) if the argument's
          length is less than x.
    """

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
