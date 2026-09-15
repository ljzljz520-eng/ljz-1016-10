import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import type { ReactNode } from "react";
import { api } from "../lib/api";
import type { User } from "../lib/types";

interface AuthState {
  user: User | null;
  /** 首次会话探测是否完成 */
  ready: boolean;
  login: (username: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthState | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [ready, setReady] = useState(false);

  useEffect(() => {
    // 启动时先取 CSRF Cookie，再探测现有会话
    (async () => {
      try {
        await api.get("/api/auth/csrf/");
        const data = await api.get<{ user: User }>("/api/auth/me/");
        setUser(data.user);
      } catch {
        setUser(null);
      } finally {
        setReady(true);
      }
    })();
  }, []);

  const login = useCallback(async (username: string, password: string) => {
    await api.get("/api/auth/csrf/");
    const data = await api.post<{ user: User }>("/api/auth/login/", { username, password });
    setUser(data.user);
  }, []);

  const logout = useCallback(async () => {
    try {
      await api.post("/api/auth/logout/");
    } finally {
      setUser(null);
    }
  }, []);

  const value = useMemo(() => ({ user, ready, login, logout }), [user, ready, login, logout]);
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthState {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth 必须在 <AuthProvider> 内使用");
  return ctx;
}
