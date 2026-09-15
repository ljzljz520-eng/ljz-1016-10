"""视图装饰器。"""
from __future__ import annotations

import functools

from .http import error


def require_methods(*methods: str):
    """限制 HTTP 方法。"""
    allowed = {m.upper() for m in methods}

    def decorator(view_func):
        @functools.wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.method not in allowed:
                return error("方法不允许", code="method_not_allowed", status=405)
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator


def login_required_json(view_func):
    """要求登录的 API，未登录返回 401 JSON（而非重定向）。"""

    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return error("未登录或会话已过期", code="unauthenticated", status=401)
        return view_func(request, *args, **kwargs)

    return wrapper


def staff_required_json(view_func):
    """要求管理员权限的 API。"""

    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return error("未登录或会话已过期", code="unauthenticated", status=401)
        if not request.user.is_staff:
            return error("没有权限执行该操作", code="forbidden", status=403)
        return view_func(request, *args, **kwargs)

    return wrapper
