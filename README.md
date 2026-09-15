# 楼宇运维管理平台（Building Ops）

楼宇系统运维后台：Django 会话认证 + HeroUI 前端，含登录失败保护、审计日志、
运维总览首页（电梯 / 空调 / 门禁三张卡片）。

## 技术栈

| 端 | 技术 |
| --- | --- |
| 后端 | Django 5.1（会话认证，无 DRF，纯 JSON API） |
| 前端 | Vite + React 18 + TypeScript + HeroUI + Tailwind CSS |
| 数据库 | SQLite（开发默认，可切换 PostgreSQL） |

## 快速开始

```bash
# 1. 后端（Python 3.11+）
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser        # 或直接使用演示账号
python manage.py runserver 127.0.0.1:8000

# 2. 前端（Node 20+）
cd frontend
npm install
npm run dev                              # http://localhost:5173
```

演示账号：`admin` / `admin123456`（仅限本地开发，生产环境请立即修改）。

前端开发服务器将 `/api` 代理到 `127.0.0.1:8000`，同源请求无跨域问题。

## 目录结构

```
backend/
├── config/                 # 项目配置（settings / 主路由）
└── apps/
    ├── core/               # 共享：统一 JSON 响应、登录/权限装饰器、请求工具
    ├── accounts/           # 认证：登录/登出/me/CSRF + 登录失败保护
    ├── audit/              # 审计日志：模型 + record_audit() + 查询 API
    └── dashboard/          # 首页总览：模块注册表（registry 模式）
frontend/src/
├── lib/                    # api 客户端（自动带 CSRF）、类型定义
├── auth/                   # AuthContext 会话状态、RequireAuth 路由守卫
├── layouts/AppLayout.tsx   # 登录后主布局（侧边栏 + 顶栏）
└── pages/                  # 登录页 / 总览页 / 审计日志页 / modules 占位页
```

## 安全机制

- **会话认证**：`HttpOnly` Cookie + CSRF Token（`X-CSRFToken` 头），会话 8 小时，活跃自动续期。
- **登录失败保护**：同一用户名或 IP 在 10 分钟内失败 5 次，锁定 10 分钟（返回 429 与
  `retry_after`）；锁定期间即使密码正确也拒绝；成功登录后重置计数。
  参数见 `settings.py` 的 `LOGIN_FAILURE_*`。
- **审计日志**：登录成功 / 失败 / 锁定 / 登出全部落库（用户、IP、UA、时间），
  业务模块可调用 `apps.audit.services.record_audit()` 记录自定义操作；
  日志在 Django Admin 中只读。

## API 一览

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/api/auth/csrf/` | 下发 CSRF Cookie |
| POST | `/api/auth/login/` | 登录（JSON: username, password） |
| POST | `/api/auth/logout/` | 登出 |
| GET | `/api/auth/me/` | 当前用户 |
| GET | `/api/dashboard/overview/` | 首页三模块汇总 |
| GET | `/api/audit/logs/` | 审计日志分页（仅管理员） |

统一响应：成功 `{"ok": true, "data": ...}`；失败 `{"ok": false, "error": {code, message, ...}}`。

## 如何接入真实模块（以电梯为例）

**后端**：新建 app 并注册总览 provider——

```bash
python manage.py startapp elevator apps/elevator   # 手动补 apps/elevator/__init__.py 路径
```

```python
# apps/elevator/apps.py
class ElevatorConfig(AppConfig):
    name = "apps.elevator"
    def ready(self):
        from apps.dashboard.registry import register_module
        from .services import get_summary
        register_module(get_summary)     # 首页卡片数据替换为真实数据源
```

在 `config/urls.py` 追加 `path("api/elevator/", include("apps.elevator.urls"))`，
并删除 `apps/dashboard/providers.py` 中对应的演示 provider。

**前端**：

1. `src/App.tsx` 增加 `<Route path="modules/elevator" element={<ElevatorPage />} />`；
2. `src/pages/DashboardPage.tsx` 的 `MODULE_THEME` 已有 elevator 图标，新 key 需补充；
3. 侧边栏在 `src/layouts/AppLayout.tsx` 的 `NAV_ITEMS` 中已内置三项，按需扩展。

## 生产部署注意

- 设置强随机 `SECRET_KEY`、`DEBUG = False`；
- 跨域部署前端时配置 `CSRF_TRUSTED_ORIGINS`，并开启 `SESSION_COOKIE_SECURE` / `CSRF_COOKIE_SECURE`；
- 建议迁移到 PostgreSQL，并将登录保护计数迁移到 Redis（当前为数据库实现，规模小可直接用）。
