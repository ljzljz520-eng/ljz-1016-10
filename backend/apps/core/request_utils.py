"""请求上下文工具（IP、UA 提取），供审计与登录保护使用。"""
from __future__ import annotations


def get_client_ip(request) -> str:
    """获取客户端 IP。反向代理部署时依赖 X-Forwarded-For 第一个地址。"""
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        return xff.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "")


def get_user_agent(request) -> str:
    return request.META.get("HTTP_USER_AGENT", "")[:500]
