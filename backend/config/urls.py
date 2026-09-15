"""主路由：所有 API 挂在 /api/ 前缀下（前端经 Vite 代理同源访问）。"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("apps.accounts.urls")),
    path("api/audit/", include("apps.audit.urls")),
    path("api/dashboard/", include("apps.dashboard.urls")),
    # 后续真实模块在此追加：
    # path("api/elevator/", include("apps.elevator.urls")),
    # path("api/hvac/", include("apps.hvac.urls")),
    # path("api/access_control/", include("apps.access_control.urls")),
]
