import React from 'react';
import { Form, Input, Select, Button, Row, Col } from 'antd';
import { AnalysisRequest } from '../types';

interface Props {
  onSubmit: (values: Partial<AnalysisRequest>) => void;
  loading: boolean;
}

export const InputForm: React.FC<Props> = ({ onSubmit, loading }) => {
  const [form] = Form.useForm();

  const handleFinish = (values: any) => {
    const competitors = values.competitors_raw.split(',').map((s: string) => s.trim()).filter(Boolean);
    const focus_areas = values.focus_raw ? values.focus_raw.split(',').map((s: string) => s.trim()).filter(Boolean) : [];
    
    onSubmit({
      ...values,
      competitors,
      focus_areas,
    });
  };

  return (
    <Form form={form} layout="vertical" onFinish={handleFinish} initialValues={{ depth: 'standard', target_audience: '产品团队' }}>
      <Row gutter={24}>
        <Col span={12}>
          <Form.Item label="你的产品名称" name="our_product" rules={[{ required: true }]}>
            <Input placeholder="如: Cursor" />
          </Form.Item>
          <Form.Item label="产品一句话描述" name="our_description">
            <Input placeholder="如: AI驱动的智能代码编辑器" />
          </Form.Item>
          <Form.Item label="竞品列表 (逗号分隔)" name="competitors_raw" rules={[{ required: true }]}>
            <Input placeholder="如: GitHub Copilot, Windsurf" />
          </Form.Item>
        </Col>
        <Col span={12}>
          <Form.Item label="所属行业" name="industry">
            <Input placeholder="如: AI编程工具" />
          </Form.Item>
          <Form.Item label="重点关注维度 (逗号分隔)" name="focus_raw">
            <Input placeholder="如: AI能力, 定价策略" />
          </Form.Item>
          <Form.Item label="分析深度" name="depth">
            <Select>
              <Select.Option value="quick">⚡ 快速 (2-3min)</Select.Option>
              <Select.Option value="standard">📊 标准 (5-8min)</Select.Option>
              <Select.Option value="deep">🔬 深度 (10-15min)</Select.Option>
            </Select>
          </Form.Item>
          <Form.Item label="报告读者" name="target_audience">
            <Input />
          </Form.Item>
        </Col>
      </Row>
      <Form.Item>
        <Button type="primary" htmlType="submit" loading={loading} size="large" block>
          🚀 开始分析
        </Button>
      </Form.Item>
    </Form>
  );
};
