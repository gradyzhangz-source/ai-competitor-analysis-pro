import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Card, Spin, message, Button } from 'antd';
import { ArrowLeftOutlined } from '@ant-design/icons';
import { ResultTabs } from '../components/ResultTabs';
import { API_BASE, isApiConfigured } from '../api/client';
import { Alert } from 'antd';

export const ReportDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [state, setState] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchTask = async () => {
      if (!isApiConfigured() || !id) {
        setLoading(false);
        return;
      }
      try {
        const res = await fetch(`${API_BASE}/tasks/${id}`);
        const data = await res.json();
        if (data.status === 'completed' && data.result_data) {
          setState(data.result_data);
        } else {
          message.error('报告未完成或数据丢失');
        }
      } catch (e) {
        message.error('获取报告详情失败');
      } finally {
        setLoading(false);
      }
    };
    fetchTask();
  }, [id]);

  if (!isApiConfigured()) {
    return (
      <Alert
        type="warning"
        showIcon
        message="未配置后端 API"
        description="请设置仓库 Secret VITE_API_BASE 后重新部署 GitHub Pages。"
      />
    );
  }

  if (loading) return <Spin size="large" style={{ display: 'block', margin: '100px auto' }} />;
  if (!state) return <div>报告不存在</div>;

  return (
    <div>
      <Button icon={<ArrowLeftOutlined />} onClick={() => navigate('/history')} style={{ marginBottom: 16 }}>
        返回历史记录
      </Button>
      <Card>
        <ResultTabs state={state} />
      </Card>
    </div>
  );
};
