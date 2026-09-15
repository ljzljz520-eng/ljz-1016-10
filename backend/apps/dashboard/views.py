"""首页总览 API。"""
from __future__ import annotations

from apps.core.decorators import login_required_json, require_methods
from apps.core.http import ok

from .registry import collect_modules


@require_methods("GET")
@login_required_json
def overview(request):
    return ok({"modules": collect_modules()})
