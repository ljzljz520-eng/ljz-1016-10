"""内置演示数据 provider。

接入真实系统后，将对应 provider 移到各业务 app 中并替换数据源，
此处演示数据可删除。
"""
from __future__ import annotations

from .registry import register_module


def _elevator_summary() -> dict:
    return {
        "key": "elevator",
        "name": "电梯系统",
        "description": "电梯运行监控、故障告警与维保管理",
        "status": "warning",
        "metrics": [
            {"label": "设备总数", "value": 24},
            {"label": "在线运行", "value": 22},
            {"label": "当前告警", "value": 1},
        ],
        "path": "/modules/elevator",
    }


def _hvac_summary() -> dict:
    return {
        "key": "hvac",
        "name": "空调系统",
        "description": "中央空调机组监控与能耗管理",
        "status": "normal",
        "metrics": [
            {"label": "机组数量", "value": 8},
            {"label": "运行中", "value": 6},
            {"label": "当前告警", "value": 0},
        ],
        "path": "/modules/hvac",
    }


def _access_control_summary() -> dict:
    return {
        "key": "access-control",
        "name": "门禁系统",
        "description": "门禁点位监控、权限与通行记录",
        "status": "normal",
        "metrics": [
            {"label": "门禁点位", "value": 56},
            {"label": "在线", "value": 55},
            {"label": "今日通行", "value": 1286},
        ],
        "path": "/modules/access-control",
    }


register_module(_elevator_summary)
register_module(_hvac_summary)
register_module(_access_control_summary)
