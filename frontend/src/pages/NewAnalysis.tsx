import React, { useState, useEffect } from 'react';
import { Card, message } from 'antd';
import { InputForm } from '../components/InputForm';
import { PipelineStatus } from '../components/PipelineStatus';
import { ResultTabs } from '../components/ResultTabs';
import { useAnalysis } from '../hooks/useAnalysis';
import { fetchConfig } from '../api/client';
import { LLMConfig } from '../types';

export const NewAnalysis: React.FC = () => {
  const [llmConfig, setLlmConfig] = useState<LLMConfig>({
    provider: 'openai',
    api_key: '',
    model: 'gpt-4o',
    base_url: 'https://api.openai.com/v1',
    tavily_api_key: '',
    serper_api_key: '',
  });

  const { isRunning, progress, result, error, startAnalysis } = useAnalysis();

  useEffect(() => {
    fetchConfig().then(cfg => {
      setLlmConfig(prev => ({
        ...prev,
        provider: cfg.llm_provider,
        api_key: cfg.llm_config[cfg.llm_provider]?.api_key || '',
        model: cfg.llm_config[cfg.llm_provider]?.model || '',
        base_url: cfg.llm_config[cfg.llm_provider]?.base_url || '',
      }));
    }).catch(console.error);
  }, []);

  useEffect(() => {
    if (error) {
      message.error(`分析失败: ${error}`);
    }
  }, [error]);

  const handleSubmit = (values: any) => {
    if (!llmConfig.api_key) {
      message.error('请在配置中设置 API Key');
      return;
    }
    startAnalysis({ ...values, llm_config: llmConfig });
  };

  return (
    <div>
      <Card style={{ marginBottom: 24 }}>
        <InputForm onSubmit={handleSubmit} loading={isRunning} />
      </Card>

      {(isRunning || progress.length > 0) && (
        <Card style={{ marginBottom: 24 }}>
          <PipelineStatus progress={progress} />
        </Card>
      )}

      {result && (
        <Card>
          <ResultTabs state={result} />
        </Card>
      )}
    </div>
  );
};
