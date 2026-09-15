import { Navigate, Route, Routes } from "react-router-dom";
import RequireAuth from "./auth/RequireAuth";
import AppLayout from "./layouts/AppLayout";
import AuditLogsPage from "./pages/AuditLogsPage";
import DashboardPage from "./pages/DashboardPage";
import LoginPage from "./pages/LoginPage";
import ModulePlaceholder from "./pages/modules/ModulePlaceholder";

/**
 * 路由表：新增业务模块时在受保护区域内追加 <Route> 即可。
 */
export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route element={<RequireAuth />}>
        <Route element={<AppLayout />}>
          <Route index element={<DashboardPage />} />
          <Route path="modules/elevator" element={<ModulePlaceholder title="电梯系统" />} />
          <Route path="modules/hvac" element={<ModulePlaceholder title="空调系统" />} />
          <Route path="modules/access-control" element={<ModulePlaceholder title="门禁系统" />} />
          <Route path="audit" element={<AuditLogsPage />} />
        </Route>
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
