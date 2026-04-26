import React from 'react';
import { Layout, Menu, Typography, Alert } from 'antd';
import { PlusOutlined, HistoryOutlined } from '@ant-design/icons';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import { isApiConfigured } from '../api/client';

const { Header, Sider, Content } = Layout;
const { Title } = Typography;

export const ProLayout: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const showPagesHint = !import.meta.env.DEV && !isApiConfigured();

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sider theme="light" style={{ borderRight: '1px solid #f0f0f0' }}>
        <div style={{ height: 64, display: 'flex', alignItems: 'center', justifyContent: 'center', borderBottom: '1px solid #f0f0f0' }}>
          <Title level={4} style={{ margin: 0, color: '#1890ff' }}>PM Agent Pro</Title>
        </div>
        <Menu
          mode="inline"
          selectedKeys={[location.pathname]}
          style={{ borderRight: 0 }}
          items={[
            {
              key: '/',
              icon: <PlusOutlined />,
              label: '新建分析',
              onClick: () => navigate('/')
            },
            {
              key: '/history',
              icon: <HistoryOutlined />,
              label: '历史记录',
              onClick: () => navigate('/history')
            }
          ]}
        />
      </Sider>
      <Layout>
        <Header style={{ background: '#fff', padding: '0 24px', borderBottom: '1px solid #f0f0f0' }}>
          <Title level={4} style={{ lineHeight: '64px', margin: 0 }}>AI 竞品分析平台</Title>
        </Header>
        <Content style={{ padding: '24px', margin: 0, minHeight: 280, background: '#f5f5f5' }}>
          {showPagesHint && (
            <Alert
              type="info"
              showIcon
              closable
              style={{ marginBottom: 16 }}
              message="GitHub Pages 静态站"
              description="分析接口需独立部署 FastAPI。请在仓库 Settings → Secrets and variables → Actions 中创建 Secret：名称 VITE_API_BASE，值为你的 API 根地址（如 https://xxx.railway.app，不要带结尾 /api），保存后重新运行「Deploy GitHub Pages」工作流。"
            />
          )}
          <Outlet />
        </Content>
      </Layout>
    </Layout>
  );
};
