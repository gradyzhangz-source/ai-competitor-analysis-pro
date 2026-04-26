import { AnalysisRequest } from '../types';

/**
 * 开发: Vite 代理到本地 FastAPI
 * 生产: 在构建时通过 VITE_API_BASE 注入已部署的 API 根（不含 /api，例如 https://api.example.com），最终请求 https://.../api/...
 * GitHub Pages 纯静态无后端时：请在仓库 Secret 里配置 VITE_API_BASE 指向你的云主机 API
 */
function resolveApiBase(): string {
  if (import.meta.env.DEV) return '/api';
  const root = import.meta.env.VITE_API_BASE?.toString().trim();
  if (!root) return '';
  return `${root.replace(/\/$/, '')}/api`;
}

export const API_BASE = resolveApiBase();

/** 生产环境且未设置 VITE_API_BASE 时无法调用分析接口 */
export const isApiConfigured = () => import.meta.env.DEV || API_BASE.length > 0;

export async function fetchConfig() {
  if (!isApiConfigured()) throw new Error('未配置 VITE_API_BASE，无法拉取配置');
  const res = await fetch(`${API_BASE}/config`);
  if (!res.ok) throw new Error('Failed to fetch config');
  return res.json();
}

export async function fetchReports() {
  if (!isApiConfigured()) throw new Error('未配置 VITE_API_BASE');
  const res = await fetch(`${API_BASE}/reports`);
  if (!res.ok) throw new Error('Failed to fetch reports');
  return res.json();
}

export async function downloadReport(filename: string) {
  if (!isApiConfigured()) return;
  window.open(`${API_BASE}/reports/${filename}`, '_blank');
}

export async function startAnalysisStream(
  request: AnalysisRequest,
  onProgress: (data: any) => void,
  onResult: (data: any) => void,
  onError: (err: any) => void
) {
  if (!isApiConfigured()) {
    onError(
      new Error(
        '未配置后端地址：请在 GitHub 仓库 Settings → Secrets → Actions 中新增 VITE_API_BASE 为你的 FastAPI 根 URL（如 https://xxx.railway.app），然后重新运行 Deploy GitHub Pages 工作流。'
      )
    );
    return;
  }
  try {
    const response = await fetch(`${API_BASE}/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const reader = response.body?.getReader();
    const decoder = new TextDecoder();

    if (!reader) throw new Error('No reader available');

    let buffer = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n\n');
      buffer = lines.pop() || '';

      for (const block of lines) {
        if (!block.trim()) continue;
        const eventMatch = block.match(/event: (.*)\n/);
        const dataMatch = block.match(/data: (.*)/);

        if (eventMatch && dataMatch) {
          const event = eventMatch[1];
          const dataStr = dataMatch[1];
          try {
            const data = JSON.parse(dataStr);
            if (event === 'progress') {
              onProgress(data);
            } else if (event === 'result') {
              onResult(data);
            } else if (event === 'error') {
              onError(data);
            }
          } catch (e) {
            console.error('Error parsing SSE data', e);
          }
        }
      }
    }
  } catch (err) {
    onError(err);
  }
}
