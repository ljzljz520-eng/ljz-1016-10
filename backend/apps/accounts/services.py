"""登录失败保护（防暴力破解）。

策略：
- 统计同一 用户名 或 同一 IP 在最近 LOGIN_FAILURE_WINDOW_MINUTES 分钟内的失败次数；
- 达到 LOGIN_FAILURE_LIMIT 次后锁定 LOGIN_LOCKOUT_MINUTES 分钟；
- 登录成功后清除该用户名+IP 的失败计数（历史记录保留用于审计）。
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta

from django.conf import settings
from django.db.models import Q
from django.utils import timezone

from .models import LoginAttempt


@dataclass
class LockStatus:
    locked: bool
    remaining_seconds: int = 0
    failure_count: int = 0


def _failure_queryset(username: str, ip: str):
    """窗口内、自上次成功之后的失败记录（用户名 或 IP 维度）。"""
    window_start = timezone.now() - timedelta(minutes=settings.LOGIN_FAILURE_WINDOW_MINUTES)
    scope = Q(username__iexact=username) | Q(ip_address=ip)
    qs = LoginAttempt.objects.filter(scope, created_at__gte=window_start)

    last_success = (
        qs.filter(success=True).order_by("-created_at").values_list("created_at", flat=True).first()
    )
    failures = qs.filter(success=False)
    if last_success:
        failures = failures.filter(created_at__gt=last_success)
    return failures


def check_lock(username: str, ip: str) -> LockStatus:
    """检查当前 用户名/IP 是否处于锁定状态。"""
    failures = _failure_queryset(username, ip)
    count = failures.count()
    if count < settings.LOGIN_FAILURE_LIMIT:
        return LockStatus(locked=False, failure_count=count)

    earliest = failures.order_by("created_at").first()
    unlock_at = earliest.created_at + timedelta(minutes=settings.LOGIN_LOCKOUT_MINUTES)
    now = timezone.now()
    if now >= unlock_at:
        return LockStatus(locked=False, failure_count=count)
    return LockStatus(
        locked=True,
        remaining_seconds=int((unlock_at - now).total_seconds()),
        failure_count=count,
    )


def record_attempt(username: str, ip: str, success: bool) -> None:
    LoginAttempt.objects.create(username=username, ip_address=ip or None, success=success)


def remaining_attempts(username: str, ip: str) -> int:
    """剩余可用尝试次数（用于前端提示）。"""
    count = _failure_queryset(username, ip).count()
    return max(settings.LOGIN_FAILURE_LIMIT - count, 0)
