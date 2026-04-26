import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { ProLayout } from './layouts/ProLayout';
import { NewAnalysis } from './pages/NewAnalysis';
import { History } from './pages/History';
import { ReportDetail } from './pages/ReportDetail';

// GitHub Pages 子路径部署时，需与 Vite `base` 一致（Vite 会注入 import.meta.env.BASE_URL）
const routerBasename =
  import.meta.env.BASE_URL === '/' ? undefined : import.meta.env.BASE_URL.replace(/\/$/, '');

const App: React.FC = () => {
  return (
    <BrowserRouter basename={routerBasename}>
      <Routes>
        <Route path="/" element={<ProLayout />}>
          <Route index element={<NewAnalysis />} />
          <Route path="history" element={<History />} />
          <Route path="report/:id" element={<ReportDetail />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
};

export default App;
