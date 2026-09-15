import { NavLink, Outlet, useNavigate } from "react-router-dom";
import {
  Avatar,
  Dropdown,
  DropdownItem,
  DropdownMenu,
  DropdownTrigger,
} from "@heroui/react";
import {
  AirVent,
  Building2,
  DoorOpen,
  LayoutDashboard,
  LogOut,
  MoveVertical,
  ScrollText,
} from "lucide-react";
import { useAuth } from "../auth/AuthContext";

/** 侧边导航：后续新增模块时在 NAV_ITEMS 追加一项即可 */
const NAV_ITEMS = [
  { to: "/", label: "运维总览", icon: LayoutDashboard, end: true },
  { to: "/modules/elevator", label: "电梯系统", icon: MoveVertical },
  { to: "/modules/hvac", label: "空调系统", icon: AirVent },
  { to: "/modules/access-control", label: "门禁系统", icon: DoorOpen },
  { to: "/audit", label: "审计日志", icon: ScrollText, staffOnly: true },
];

export default function AppLayout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate("/login", { replace: true });
  };

  return (
    <div className="flex h-screen bg-default-50">
      {/* 侧边栏 */}
      <aside className="flex w-60 shrink-0 flex-col border-r border-default-200 bg-white">
        <div className="flex h-16 items-center gap-2 border-b border-default-200 px-5">
          <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-primary text-white">
            <Building2 size={20} />
          </div>
          <div>
            <div className="text-sm font-bold leading-tight">楼宇运维管理平台</div>
            <div className="text-xs text-default-400">Building Ops</div>
          </div>
        </div>
        <nav className="flex-1 space-y-1 overflow-y-auto p-3">
          {NAV_ITEMS.filter((item) => !item.staffOnly || user?.is_staff).map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.end}
              className={({ isActive }) =>
                `flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm transition-colors ${
                  isActive
                    ? "bg-primary font-medium text-white"
                    : "text-default-600 hover:bg-default-100"
                }`
              }
            >
              <item.icon size={18} />
              {item.label}
            </NavLink>
          ))}
        </nav>
      </aside>

      {/* 主区域 */}
      <div className="flex min-w-0 flex-1 flex-col">
        {/* 顶栏 */}
        <header className="flex h-16 shrink-0 items-center justify-between border-b border-default-200 bg-white px-6">
          <div className="text-sm text-default-500">智慧楼宇 · 运维后台</div>
          <Dropdown placement="bottom-end">
            <DropdownTrigger>
              <button className="flex items-center gap-2 rounded-full px-2 py-1 transition-colors hover:bg-default-100">
                <Avatar
                  size="sm"
                  name={user?.display_name ?? user?.username}
                  className="bg-primary text-white"
                />
                <span className="text-sm font-medium">{user?.display_name}</span>
              </button>
            </DropdownTrigger>
            <DropdownMenu aria-label="用户菜单">
              <DropdownItem key="profile" isReadOnly textValue="账号信息">
                <div className="flex flex-col">
                  <span className="text-sm font-medium">{user?.display_name}</span>
                  <span className="text-xs text-default-400">@{user?.username}</span>
                </div>
              </DropdownItem>
              <DropdownItem
                key="logout"
                color="danger"
                startContent={<LogOut size={16} />}
                onPress={handleLogout}
              >
                退出登录
              </DropdownItem>
            </DropdownMenu>
          </Dropdown>
        </header>

        {/* 内容区 */}
        <main className="min-h-0 flex-1 overflow-y-auto p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
