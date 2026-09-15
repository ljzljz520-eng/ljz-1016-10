"""审计日志写入入口。

用法（任何业务模块都可以调用）：
    from apps.audit.services import record_audit
    record_audit(request, AuditLog.Action.UPDATE, detail={"target": "elevator-01"})
"""
from __future__ import annotations

import logging
from typing import Any

from apps.core.request_utils import get_client_ip, get_user_agent

from .models import AuditLog

logger = logging.getLogger(__name__)


def record_audit(
    request,
    action: str,
    *,
    status: str = AuditLog.Status.SUCCESS,
    user=None,
    username: str = "",
    detail: dict[str, Any] | None = None,
) -> AuditLog | None:
    """写入一条审计日志。写日志失败不应影响主流程，故捕获异常。"""
    try:
        resolved_user = user
        if resolved_user is None and getattr(request, "user", None) is not None:
            if request.user.is_authenticated:
                resolved_user = request.user

        resolved_username = username
        if not resolved_username and resolved_user is not None:
            resolved_username = resolved_user.get_username()

        return AuditLog.objects.create(
            user=resolved_user,
            username=resolved_username,
            action=action,
            status=status,
            detail=detail or {},
            ip_address=get_client_ip(request) or None,
            user_agent=get_user_agent(request),
        )
    except Exception:  # noqa: BLE001 - 审计失败不阻断业务
        logger.exception("写入审计日志失败")
        return None
