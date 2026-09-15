"""会话认证 API：CSRF 下发 / 登录 / 登出 / 当前用户。"""
from __future__ import annotations

from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie

from apps.audit.models import AuditLog
from apps.audit.services import record_audit
from apps.core.decorators import login_required_json, require_methods
from apps.core.http import error, ok, parse_json_body
from apps.core.request_utils import get_client_ip

from . import services


def _user_payload(user) -> dict:
    display_name = user.get_full_name() or user.get_username()
    return {
        "id": user.id,
        "username": user.get_username(),
        "display_name": display_name,
        "is_staff": user.is_staff,
    }


@require_methods("GET")
@ensure_csrf_cookie
def csrf(request):
    """前端启动时调用，确保 csrftoken Cookie 已下发。"""
    return ok({"csrf_token": get_token(request)})


@require_methods("POST")
def login_view(request):
    body, err = parse_json_body(request)
    if err:
        return err

    username = (body.get("username") or "").strip()
    password = body.get("password") or ""
    if not username or not password:
        return error("请输入用户名和密码", code="missing_credentials", status=400)

    ip = get_client_ip(request)

    # 1. 锁定检查（失败保护）
    lock = services.check_lock(username, ip)
    if lock.locked:
        record_audit(
            request,
            AuditLog.Action.LOGIN_LOCKED,
            status=AuditLog.Status.FAILURE,
            username=username,
            detail={"remaining_seconds": lock.remaining_seconds},
        )
        return error(
            f"失败次数过多，账号已临时锁定，请 {max(lock.remaining_seconds // 60, 1)} 分钟后重试",
            code="login_locked",
            status=429,
            retry_after=lock.remaining_seconds,
        )

    # 2. 认证
    user = authenticate(request, username=username, password=password)
    if user is None:
        services.record_attempt(username, ip, success=False)
        left = services.remaining_attempts(username, ip)
        record_audit(
            request,
            AuditLog.Action.LOGIN_FAILED,
            status=AuditLog.Status.FAILURE,
            username=username,
            detail={"reason": "用户名或密码错误", "remaining_attempts": left},
        )
        return error(
            "用户名或密码错误" + (f"，剩余尝试次数 {left} 次" if left <= 3 else ""),
            code="invalid_credentials",
            status=401,
            remaining_attempts=left,
        )

    if not user.is_active:
        record_audit(
            request,
            AuditLog.Action.LOGIN_FAILED,
            status=AuditLog.Status.FAILURE,
            username=username,
            detail={"reason": "账号已停用"},
        )
        return error("账号已停用，请联系管理员", code="user_inactive", status=403)

    # 3. 建立会话
    services.record_attempt(username, ip, success=True)
    login(request, user)
    record_audit(request, AuditLog.Action.LOGIN, user=user)
    return ok({"user": _user_payload(user)})


@require_methods("POST")
@login_required_json
def logout_view(request):
    record_audit(request, AuditLog.Action.LOGOUT)
    logout(request)
    return ok({"message": "已退出登录"})


@require_methods("GET")
@login_required_json
def me(request):
    return ok({"user": _user_payload(request.user)})
