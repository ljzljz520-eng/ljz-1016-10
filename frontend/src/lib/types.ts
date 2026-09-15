/** 与后端约定一致的 API 类型定义 */

export interface User {
  id: number;
  username: string;
  display_name: string;
  is_staff: boolean;
}

export interface ModuleMetric {
  label: string;
  value: number | string;
}

export type ModuleStatus = "normal" | "warning" | "critical" | "offline";

export interface ModuleSummary {
  key: string;
  name: string;
  description: string;
  status: ModuleStatus;
  metrics: ModuleMetric[];
  path: string;
}

export interface AuditLogItem {
  id: number;
  username: string;
  action: string;
  action_display: string;
  status: "success" | "failure";
  detail: Record<string, unknown>;
  ip_address: string | null;
  user_agent: string;
  created_at: string;
}

export interface PagedResult<T> {
  total: number;
  page: number;
  page_size: number;
  results: T[];
}
