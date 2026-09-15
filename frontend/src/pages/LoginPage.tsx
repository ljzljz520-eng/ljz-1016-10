import { useState } from "react";
import type { FormEvent } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { Button, Card, CardBody, CardHeader, Input } from "@heroui/react";
import { Building2, Lock, User } from "lucide-react";
import { useAuth } from "../auth/AuthContext";
import { ApiError } from "../lib/api";

export default function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation() as { state?: { from?: string } };

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (loading) return;
    setError("");
    setLoading(true);
    try {
      await login(username.trim(), password);
      navigate(location.state?.from ?? "/", { replace: true });
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "登录失败，请稍后重试");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-slate-100 via-blue-50 to-slate-100 px-4">
      <Card className="w-full max-w-md shadow-lg">
        <CardHeader className="flex flex-col items-center gap-3 pb-0 pt-8">
          <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-primary text-white">
            <Building2 size={30} />
          </div>
          <div className="text-center">
            <h1 className="text-xl font-bold">楼宇运维管理平台</h1>
            <p className="mt-1 text-sm text-default-500">Building Operations Management</p>
          </div>
        </CardHeader>
        <CardBody className="px-8 py-8">
          <form onSubmit={onSubmit} className="flex flex-col gap-4">
            <Input
              label="用户名"
              placeholder="请输入用户名"
              value={username}
              onValueChange={setUsername}
              startContent={<User size={16} className="text-default-400" />}
              autoComplete="username"
              isRequired
            />
            <Input
              label="密码"
              type="password"
              placeholder="请输入密码"
              value={password}
              onValueChange={setPassword}
              startContent={<Lock size={16} className="text-default-400" />}
              autoComplete="current-password"
              isRequired
            />
            {error && (
              <div className="rounded-lg bg-danger-50 px-3 py-2 text-sm text-danger">{error}</div>
            )}
            <Button
              type="submit"
              color="primary"
              size="lg"
              isLoading={loading}
              isDisabled={!username || !password}
              className="mt-2"
            >
              登 录
            </Button>
          </form>
        </CardBody>
      </Card>
    </div>
  );
}
