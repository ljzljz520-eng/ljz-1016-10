"""登录尝试记录：用于登录失败保护（锁定策略）。"""
from __future__ import annotations

from django.db import models


class LoginAttempt(models.Model):
    username = models.CharField("用户名", max_length=150, db_index=True)
    ip_address = models.GenericIPAddressField("IP 地址", null=True, blank=True, db_index=True)
    success = models.BooleanField("是否成功", default=False)
    created_at = models.DateTimeField("时间", auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = "登录尝试"
        verbose_name_plural = "登录尝试"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        result = "成功" if self.success else "失败"
        return f"{self.username} {result} @ {self.created_at:%Y-%m-%d %H:%M:%S}"
