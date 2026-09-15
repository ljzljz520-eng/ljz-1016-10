import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button, Card, CardBody, CardFooter, CardHeader, Chip, Spinner } from "@heroui/react";
import { AirVent, ArrowRight, DoorOpen, MoveVertical } from "lucide-react";
import type { LucideIcon } from "lucide-react";
import { api } from "../lib/api";
import type { ModuleStatus, ModuleSummary } from "../lib/types";

/** 模块 key → 图标/配色的展示映射（新模块在此补充） */
const MODULE_THEME: Record<string, { icon: LucideIcon; color: string }> = {
  elevator: { icon: MoveVertical, color: "bg-blue-500" },
  hvac: { icon: AirVent, color: "bg-cyan-500" },
  "access-control": { icon: DoorOpen, color: "bg-violet-500" },
};

const STATUS_META: Record<ModuleStatus, { label: string; color: "success" | "warning" | "danger" | "default" }> = {
  normal: { label: "运行正常", color: "success" },
  warning: { label: "存在告警", color: "warning" },
  critical: { label: "严重故障", color: "danger" },
  offline: { label: "离线", color: "default" },
};

function ModuleCard({ module }: { module: ModuleSummary }) {
  const navigate = useNavigate();
  const theme = MODULE_THEME[module.key] ?? { icon: MoveVertical, color: "bg-default-400" };
  const status = STATUS_META[module.status] ?? STATUS_META.normal;
  const Icon = theme.icon;

  return (
    <Card className="shadow-sm transition-shadow hover:shadow-md">
      <CardHeader className="flex items-start justify-between px-5 pt-5 pb-0">
        <div className="flex items-center gap-3">
          <div className={`flex h-11 w-11 items-center justify-center rounded-xl text-white ${theme.color}`}>
            <Icon size={22} />
          </div>
          <div>
            <div className="text-base font-semibold">{module.name}</div>
            <div className="text-xs text-default-400">{module.description}</div>
          </div>
        </div>
        <Chip size="sm" color={status.color} variant="flat">
          {status.label}
        </Chip>
      </CardHeader>
      <CardBody className="px-5 py-4">
        <div className="grid grid-cols-3 gap-2">
          {module.metrics.map((m) => (
            <div key={m.label} className="rounded-lg bg-default-50 px-3 py-2 text-center">
              <div className="text-xl font-bold">{m.value}</div>
              <div className="text-xs text-default-400">{m.label}</div>
            </div>
          ))}
        </div>
      </CardBody>
      <CardFooter className="px-5 pb-4 pt-0">
        <Button
          size="sm"
          variant="light"
          color="primary"
          endContent={<ArrowRight size={14} />}
          onPress={() => navigate(module.path)}
        >
          进入模块
        </Button>
      </CardFooter>
    </Card>
  );
}

export default function DashboardPage() {
  const [modules, setModules] = useState<ModuleSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    api
      .get<{ modules: ModuleSummary[] }>("/api/dashboard/overview/")
      .then((data) => setModules(data.modules))
      .catch((err) => setError(err.message ?? "加载失败"))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-xl font-bold">运维总览</h1>
        <p className="mt-1 text-sm text-default-400">各子系统运行状态一览</p>
      </div>
      {loading ? (
        <div className="flex justify-center py-20">
          <Spinner size="lg" />
        </div>
      ) : error ? (
        <div className="rounded-lg bg-danger-50 px-4 py-3 text-sm text-danger">{error}</div>
      ) : (
        <div className="grid grid-cols-1 gap-5 md:grid-cols-2 xl:grid-cols-3">
          {modules.map((m) => (
            <ModuleCard key={m.key} module={m} />
          ))}
        </div>
      )}
    </div>
  );
}
