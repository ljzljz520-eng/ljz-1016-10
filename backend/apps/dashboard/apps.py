from django.apps import AppConfig


class DashboardConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.dashboard"
    verbose_name = "运维总览"

    def ready(self):
        # 加载内置演示 provider；后续真实模块在各自 app 的 ready() 中注册即可
        from . import providers  # noqa: F401
