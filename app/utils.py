import os
import inspect
from functools import wraps
from typing import List, Tuple

from fastapi import HTTPException


def validate_env_variables(env_var_names: List[str]) -> Tuple[str, ...]:
    """
    Validate that multiple environment variables are set and return their values.

    Args:
        env_var_names (List[str]): List of environment variable names to check

    Returns:
        Tuple[str, ...]: Tuple of environment variable values in the same order as input

    Raises:
        ValueError: If any environment variable is not set
    """
    values = []
    for var_name in env_var_names:
        value = os.getenv(var_name)
        if not value:
            raise ValueError(
                f"{var_name} environment variable is required. Please set it in your .env file."  # noqa: E501
            )
        values.append(value)

    return tuple(values)


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
