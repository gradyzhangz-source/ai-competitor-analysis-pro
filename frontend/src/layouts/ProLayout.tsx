import React from 'react';
import { Layout, Menu, Typography } from 'antd';
import { PlusOutlined, HistoryOutlined } from '@ant-design/icons';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';

const { Header, Sider, Content } = Layout;
const { Title } = Typography;

export const ProLayout: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();

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
          <Outlet />
        </Content>
      </Layout>
    </Layout>
  );
};
