/** 统一 API 客户端：同源请求 + CSRF 头 + 标准错误 */

export class ApiError extends Error {
  status: number;
  code: string;
  extra: Record<string, unknown>;

  constructor(status: number, code: string, message: string, extra: Record<string, unknown> = {}) {
    super(message);
    this.status = status;
    this.code = code;
    this.extra = extra;
  }
}

function getCookie(name: string): string {
  const match = document.cookie.match(new RegExp(`(?:^|; )${name}=([^;]*)`));
  return match ? decodeURIComponent(match[1]) : "";
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const res = await fetch(path, {
    credentials: "same-origin",
    ...options,
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
      ...(options.headers ?? {}),
    },
  });

  let payload: unknown = null;
  try {
    payload = await res.json();
  } catch {
    throw new ApiError(res.status, "bad_response", `服务响应异常（HTTP ${res.status}）`);
  }

  const body = payload as {
    ok: boolean;
    data?: T;
    error?: { code: string; message: string } & Record<string, unknown>;
  };

  if (!res.ok || !body.ok) {
    const err = body.error ?? { code: "unknown", message: "未知错误" };
    throw new ApiError(res.status, err.code, err.message, err);
  }
  return body.data as T;
}

export const api = {
  get: <T>(path: string) => request<T>(path),
  post: <T>(path: string, data?: unknown) =>
    request<T>(path, { method: "POST", body: JSON.stringify(data ?? {}) }),
};
