import { Navigate, Outlet, useLocation } from "react-router-dom";
import { Spinner } from "@heroui/react";
import { useAuth } from "./AuthContext";

/** 路由守卫：未登录跳转登录页，会话探测中显示加载 */
export default function RequireAuth() {
  const { user, ready } = useAuth();
  const location = useLocation();

  if (!ready) {
    return (
      <div className="flex h-screen items-center justify-center">
        <Spinner size="lg" label="正在加载..." />
      </div>
    );
  }
  if (!user) {
    return <Navigate to="/login" replace state={{ from: location.pathname }} />;
  }
  return <Outlet />;
}
