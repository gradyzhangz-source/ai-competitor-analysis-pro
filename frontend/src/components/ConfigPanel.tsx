import React from 'react';
import { Form, Input, Select, Collapse } from 'antd';
import { LLMConfig } from '../types';

interface Props {
  value: LLMConfig;
  onChange: (val: LLMConfig) => void;
}

export const ConfigPanel: React.FC<Props> = ({ value, onChange }) => {
  const [form] = Form.useForm<LLMConfig>();

  const handleValuesChange = (_: any, allValues: LLMConfig) => {
    onChange(allValues);
  };

  return (
    <Collapse defaultActiveKey={['1', '2']} ghost>
      <Collapse.Panel header="🤖 LLM 设置" key="1">
        <Form
          form={form}
          layout="vertical"
          initialValues={value}
          onValuesChange={handleValuesChange}
        >
          <Form.Item label="LLM 服务商" name="provider">
            <Select>
              <Select.Option value="openai">OpenAI</Select.Option>
              <Select.Option value="deepseek">DeepSeek</Select.Option>
              <Select.Option value="custom">Custom</Select.Option>
            </Select>
          </Form.Item>
          <Form.Item label="API Key" name="api_key">
            <Input.Password placeholder="sk-..." />
          </Form.Item>
          <Form.Item label="模型名称" name="model">
            <Input />
          </Form.Item>
          {Form.useWatch('provider', form) === 'custom' && (
            <Form.Item label="API Base URL" name="base_url">
              <Input />
            </Form.Item>
          )}
        </Form>
      </Collapse.Panel>

      <Collapse.Panel header="🌐 搜索 API" key="2">
        <Form
          form={form}
          layout="vertical"
          initialValues={value}
          onValuesChange={handleValuesChange}
        >
          <Form.Item label="Tavily API Key" name="tavily_api_key">
            <Input.Password placeholder="tvly-..." />
          </Form.Item>
          <Form.Item label="Serper API Key" name="serper_api_key">
            <Input.Password />
          </Form.Item>
        </Form>
      </Collapse.Panel>
    </Collapse>
  );
};
