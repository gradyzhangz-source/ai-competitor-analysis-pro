import React from 'react';
import { Steps } from 'antd';
import { ProgressEvent } from '../types';

interface Props {
  progress: ProgressEvent[];
}

const STAGES = [
  { title: '信息收集', icon: '🔍' },
  { title: '深度分析', icon: '📊' },
  { title: '战略建议', icon: '🎯' },
  { title: '报告生成', icon: '📄' },
];

export const PipelineStatus: React.FC<Props> = ({ progress }) => {
  let current = 0;
  let status: 'wait' | 'process' | 'finish' | 'error' = 'wait';

  for (let i = 0; i < STAGES.length; i++) {
    const p = progress[i];
    if (p) {
      current = i;
      if (p.status === 'running') status = 'process';
      else if (p.status === 'done') {
        status = 'finish';
        current = i + 1;
      }
      else if (p.status === 'error') status = 'error';
    }
  }

  return (
    <div style={{ margin: '24px 0' }}>
      <Steps
        current={current}
        status={status as any}
        items={STAGES.map((s, i) => {
          const p = progress[i];
          return {
            title: `${s.icon} ${s.title}`,
            description: p ? p.message : '',
          };
        })}
      />
    </div>
  );
};
