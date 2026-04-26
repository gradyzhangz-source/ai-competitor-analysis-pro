/// <reference types="vite/client" />

interface ImportMetaEnv {
  /** 生产环境：已部署 FastAPI 的站点根 URL（不含 /api），与 GitHub Secrets 中 VITE_API_BASE 一致 */
  readonly VITE_API_BASE?: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
