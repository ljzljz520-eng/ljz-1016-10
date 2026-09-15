"""审计日志模型。

记录所有关键操作：登录/登出、登录失败、锁定，以及后续业务模块的
增删改操作（通过 audit.services.record() 写入）。
"""
from __future__ import annotations

from django.conf import settings
from django.db import models


class AuditLog(models.Model):
    class Action(models.TextChoices):
        LOGIN = "login", "登录成功"
        LOGIN_FAILED = "login_failed", "登录失败"
        LOGIN_LOCKED = "login_locked", "登录锁定"
        LOGOUT = "logout", "退出登录"
        CREATE = "create", "新增"
        UPDATE = "update", "修改"
        DELETE = "delete", "删除"
        OTHER = "other", "其他"

    class Status(models.TextChoices):
        SUCCESS = "success", "成功"
        FAILURE = "failure", "失败"

    # 关联用户（允许为空：登录失败时用户可能不存在；用户被删后日志保留）
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="audit_logs",
        verbose_name="操作用户",
    )
    username = models.CharField("用户名快照", max_length=150, db_index=True)
    action = models.CharField("操作类型", max_length=32, choices=Action.choices, db_index=True)
    status = models.CharField("结果", max_length=16, choices=Status.choices, default=Status.SUCCESS)
    detail = models.JSONField("详情", default=dict, blank=True)
    ip_address = models.GenericIPAddressField("IP 地址", null=True, blank=True)
    user_agent = models.CharField("User-Agent", max_length=500, blank=True, default="")
    created_at = models.DateTimeField("时间", auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = "审计日志"
        verbose_name_plural = "审计日志"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"[{self.get_action_display()}] {self.username} @ {self.created_at:%Y-%m-%d %H:%M:%S}"
