"""运维模块注册表。

后续新增真实模块（如 apps.elevator）时，在其 AppConfig.ready() 中：

    from apps.dashboard.registry import register_module
    from .services import get_summary

    def ready(self):
        register_module(get_summary)

get_summary() 需返回 dict：
{
    "key": "elevator",            # 唯一标识，与前端路由对应
    "name": "电梯系统",
    "description": "...",
    "status": "normal",           # normal | warning | critical | offline
    "metrics": [{"label": "设备总数", "value": 24}, ...],
    "path": "/modules/elevator",  # 前端路由
}
"""
from __future__ import annotations

from typing import Any, Callable

ModuleProvider = Callable[[], dict[str, Any]]

_providers: list[ModuleProvider] = []


def register_module(provider: ModuleProvider) -> None:
    _providers.append(provider)


def collect_modules() -> list[dict[str, Any]]:
    return [provider() for provider in _providers]
