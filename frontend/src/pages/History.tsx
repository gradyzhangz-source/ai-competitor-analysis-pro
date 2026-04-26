import React, { useEffect, useState } from 'react';
import { Table, Button, Space, message, Tag, Alert } from 'antd';
import { useNavigate } from 'react-router-dom';
import { API_BASE, isApiConfigured } from '../api/client';

export const History: React.FC = () => {
  const [tasks, setTasks] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const loadTasks = async () => {
    if (!isApiConfigured()) {
      setTasks([]);
      return;
    }
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/tasks`);
      const data = await res.json();
      setTasks(data);
    } catch (e) {
      message.error('获取历史记录失败');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadTasks();
  }, []);

  const handleDelete = async (id: number) => {
    if (!isApiConfigured()) return;
    try {
      await fetch(`${API_BASE}/tasks/${id}`, { method: 'DELETE' });
      message.success('删除成功');
      loadTasks();
    } catch (e) {
      message.error('删除失败');
    }
  };

  const columns = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: '产品', dataIndex: 'product_name', key: 'product_name' },
    { title: '行业', dataIndex: 'industry', key: 'industry' },
    { 
      title: '状态', 
      dataIndex: 'status', 
      key: 'status',
      render: (status: string) => {
        const color = status === 'completed' ? 'green' : status === 'failed' ? 'red' : 'blue';
        return <Tag color={color}>{status.toUpperCase()}</Tag>;
      }
    },
    { title: '创建时间', dataIndex: 'created_at', key: 'created_at', render: (t: string) => new Date(t).toLocaleString() },
    {
      title: '操作',
      key: 'action',
      render: (_: any, record: any) => (
        <Space size="middle">
          <Button type="link" onClick={() => navigate(`/report/${record.id}`)} disabled={record.status !== 'completed'}>查看报告</Button>
          <Button type="link" danger onClick={() => handleDelete(record.id)}>删除</Button>
        </Space>
      ),
    },
  ];

  if (!isApiConfigured()) {
    return (
      <Alert
        type="info"
        showIcon
        message="静态演示模式暂不保存历史记录"
        description="GitHub Pages 版本不依赖后端数据库，因此历史记录不会持久化。要启用真实历史记录，请部署 FastAPI 后端并配置 VITE_API_BASE。"
      />
    );
  }

  return <Table columns={columns} dataSource={tasks} rowKey="id" loading={loading} />;
};
