import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { ProLayout } from './layouts/ProLayout';
import { NewAnalysis } from './pages/NewAnalysis';
import { History } from './pages/History';
import { ReportDetail } from './pages/ReportDetail';

const App: React.FC = () => {
  return (
    <BrowserRouter>
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
