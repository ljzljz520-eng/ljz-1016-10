"""审计日志查询 API（仅管理员）。"""
from __future__ import annotations

from django.core.paginator import Paginator

from apps.core.decorators import require_methods, staff_required_json
from apps.core.http import ok

from .models import AuditLog


@require_methods("GET")
@staff_required_json
def audit_log_list(request):
    page = max(int(request.GET.get("page", 1) or 1), 1)
    page_size = min(max(int(request.GET.get("page_size", 20) or 20), 1), 100)
    action = request.GET.get("action", "").strip()
    keyword = request.GET.get("keyword", "").strip()

    qs = AuditLog.objects.all()
    if action:
        qs = qs.filter(action=action)
    if keyword:
        qs = qs.filter(username__icontains=keyword)

    paginator = Paginator(qs, page_size)
    page_obj = paginator.get_page(page)

    return ok(
        {
            "total": paginator.count,
            "page": page_obj.number,
            "page_size": page_size,
            "results": [
                {
                    "id": log.id,
                    "username": log.username,
                    "action": log.action,
                    "action_display": log.get_action_display(),
                    "status": log.status,
                    "detail": log.detail,
                    "ip_address": log.ip_address,
                    "user_agent": log.user_agent,
                    "created_at": log.created_at.isoformat(),
                }
                for log in page_obj.object_list
            ],
        }
    )
