"""统一 API 响应格式。

成功: {"ok": true,  "data": ...}
失败: {"ok": false, "error": {"code": "...", "message": "...", ...}}
"""
from __future__ import annotations

import json
from typing import Any

from django.http import JsonResponse


def ok(data: Any = None, status: int = 200) -> JsonResponse:
    return JsonResponse({"ok": True, "data": data}, status=status)


def error(message: str, *, code: str = "bad_request", status: int = 400, **extra: Any) -> JsonResponse:
    payload: dict[str, Any] = {"code": code, "message": message}
    payload.update(extra)
    return JsonResponse({"ok": False, "error": payload}, status=status)


def parse_json_body(request) -> tuple[dict | None, JsonResponse | None]:
    """解析 JSON 请求体，失败时返回 (None, 错误响应)。"""
    try:
        body = json.loads(request.body.decode("utf-8") or "{}")
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None, error("请求体不是合法的 JSON", code="invalid_json", status=400)
    if not isinstance(body, dict):
        return None, error("请求体必须是 JSON 对象", code="invalid_json", status=400)
    return body, None
