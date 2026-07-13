import functools
import hashlib
import json
import traceback

from fastapi import Request


def is_serializable(value):
    """Check if value is JSON-serializable"""
    if isinstance(value, (str, int, float, bool, type(None))):
        return True
    if isinstance(value, (list, tuple)):
        return all(is_serializable(item) for item in value)
    if isinstance(value, dict):
        return all(is_serializable(k) and is_serializable(v) for k, v in value.items())
    return False


def universal_key_builder(
    func,
    namespace: str = "",
    request: Request = None,
    response=None,
    *args,
    **kwargs,
):
    """
    Universal cache key builder that handles:
    - Path parameters
    - Query parameters
    - Request body (for POST/PUT/PATCH)
    - Any combination of the above
    """

    try:
        actual_kwargs = kwargs.get("kwargs", kwargs)

        cache_key_parts = [
            namespace,
            func.__module__,
            func.__name__,
        ]

        # Add request method (GET, POST, etc.)
        if request:
            cache_key_parts.append(request.method)

            # Add path with path parameters
            cache_key_parts.append(request.url.path)

            # Add query parameters (sorted for consistency)
            if request.url.query:
                query_params = str(request.url.query)
                cache_key_parts.append(f"query:{query_params}")

        # Add path parameters from kwargs
        excluded_keys = {"request", "response", "body", "service", "self", "cls"}
        path_params = {
            k: v
            for k, v in actual_kwargs.items()
            if k not in excluded_keys and is_serializable(v)
        }

        if path_params:
            path_str = json.dumps(path_params, sort_keys=True)
            path_hash = hashlib.md5(path_str.encode()).hexdigest()
            cache_key_parts.append(f"path:{path_hash}")

        # Add request body if present (for POST/PUT/PATCH)
        body = actual_kwargs.get("body")
        if body:
            # Handle Pydantic models (v2 and v1 compatible)
            if hasattr(body, "model_dump"):
                body_dict = body.model_dump(mode="json")
            elif hasattr(body, "dict"):
                body_dict = body.dict()
            else:
                body_dict = body

            body_str = json.dumps(body_dict, sort_keys=True)
            body_hash = hashlib.md5(body_str.encode()).hexdigest()
            cache_key_parts.append(f"body:{body_hash}")

        # Join all parts with colons
        cache_key = ":".join(cache_key_parts)
        return cache_key

    except Exception as e:
        print(traceback.format_exc())
        raise e


def cache_wrapper(cache_decorator):
    """
    Wraps a caching decorator and logs exceptions instead of failing.
    """

    def decorator(func):
        # Apply the original cache decorator inside try/except
        try:
            cached_func = cache_decorator(func)
        except Exception as e:
            print(traceback.format_exc())
            cached_func = func  # fallback to original function if caching fails

        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await cached_func(*args, **kwargs)
            except Exception as e:
                print(traceback.format_exc())
                return await func(*args, **kwargs)  # fallback if cache fails at runtime

        return wrapper

    return decorator