import { useCallback, useEffect, useState } from "react";
import {
  Card,
  CardBody,
  Chip,
  Pagination,
  Spinner,
  Table,
  TableBody,
  TableCell,
  TableColumn,
  TableHeader,
  TableRow,
} from "@heroui/react";
import { api } from "../lib/api";
import type { AuditLogItem, PagedResult } from "../lib/types";

const PAGE_SIZE = 15;

export default function AuditLogsPage() {
  const [data, setData] = useState<PagedResult<AuditLogItem> | null>(null);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const load = useCallback((p: number) => {
    setLoading(true);
    api
      .get<PagedResult<AuditLogItem>>(`/api/audit/logs/?page=${p}&page_size=${PAGE_SIZE}`)
      .then(setData)
      .catch((err) => setError(err.message ?? "加载失败"))
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    load(page);
  }, [page, load]);

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-xl font-bold">审计日志</h1>
        <p className="mt-1 text-sm text-default-400">系统关键操作记录（登录、登出、锁定等）</p>
      </div>
      <Card className="shadow-sm">
        <CardBody className="p-0">
          <Table
            aria-label="审计日志"
            removeWrapper
            bottomContent={
              data && data.total > PAGE_SIZE ? (
                <div className="flex justify-center py-3">
                  <Pagination
                    total={Math.ceil(data.total / PAGE_SIZE)}
                    page={page}
                    onChange={setPage}
                    size="sm"
                  />
                </div>
              ) : undefined
            }
          >
            <TableHeader>
              <TableColumn>时间</TableColumn>
              <TableColumn>用户</TableColumn>
              <TableColumn>操作</TableColumn>
              <TableColumn>结果</TableColumn>
              <TableColumn>IP 地址</TableColumn>
            </TableHeader>
            <TableBody
              items={data?.results ?? []}
              isLoading={loading}
              loadingContent={<Spinner size="sm" />}
              emptyContent={error || "暂无记录"}
            >
              {(item) => (
                <TableRow key={item.id}>
                  <TableCell className="whitespace-nowrap text-sm">
                    {new Date(item.created_at).toLocaleString("zh-CN", { hour12: false })}
                  </TableCell>
                  <TableCell>{item.username || "-"}</TableCell>
                  <TableCell>{item.action_display}</TableCell>
                  <TableCell>
                    <Chip
                      size="sm"
                      variant="flat"
                      color={item.status === "success" ? "success" : "danger"}
                    >
                      {item.status === "success" ? "成功" : "失败"}
                    </Chip>
                  </TableCell>
                  <TableCell className="text-sm text-default-500">{item.ip_address ?? "-"}</TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </CardBody>
      </Card>
    </div>
  );
}
