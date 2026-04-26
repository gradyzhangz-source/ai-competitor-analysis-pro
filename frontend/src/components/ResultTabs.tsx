import React from 'react';
import { Tabs, Card, Table, Tag, Collapse, Alert, Typography } from 'antd';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { AnalysisState } from '../types';
import { PortersRadar } from './PortersRadar';
import { SwotChart } from './SwotChart';
import { ReportEditor } from './ReportEditor';

const { Title, Paragraph } = Typography;

interface Props {
  state: AnalysisState;
}

export const ResultTabs: React.FC<Props> = ({ state }) => {
  const items = [
    {
      key: '1',
      label: '📄 完整报告',
      children: (
        <Card>
          <ReportEditor initialValue={state.final_report_md || '报告未生成'} />
        </Card>
      ),
    },
    {
      key: '2',
      label: '🏢 竞品画像',
      children: (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          {state.our_profile && (
            <Card title={`我方产品: ${state.our_profile.name}`}>
              <p><strong>定位:</strong> {state.our_profile.description}</p>
              <p><strong>目标用户:</strong> {state.our_profile.target_users}</p>
              <p><strong>定价模式:</strong> {state.our_profile.pricing_model}</p>
            </Card>
          )}
          {state.competitor_profiles.map((cp) => (
            <Card key={cp.name} title={`${cp.name} (${cp.tier}竞品)`}>
              <p><strong>定位:</strong> {cp.description}</p>
              <p><strong>优势:</strong> {cp.strengths.join('; ')}</p>
              <p><strong>劣势:</strong> {cp.weaknesses.join('; ')}</p>
            </Card>
          ))}
        </div>
      ),
    },
    {
      key: '3',
      label: '📊 SWOT',
      children: <SwotChart data={state.swot_results} />,
    },
    {
      key: '4',
      label: '🔧 功能矩阵',
      children: (
        <Table
          dataSource={state.feature_matrix.map((f, i) => ({ key: i, feature: f.feature_name, ...f.scores }))}
          columns={[
            { title: '功能点', dataIndex: 'feature', key: 'feature' },
            ...(state.our_profile ? [{ title: state.our_profile.name, dataIndex: state.our_profile.name, key: state.our_profile.name }] : []),
            ...state.competitor_profiles.map(cp => ({ title: cp.name, dataIndex: cp.name, key: cp.name }))
          ]}
          pagination={false}
        />
      ),
    },
    {
      key: '8',
      label: '⚖️ 五力分析',
      children: (
        <Card>
          <PortersRadar data={state.porters} />
        </Card>
      ),
    },
    {
      key: '5',
      label: '🎯 战略建议',
      children: (
        <div>
          {state.competitive_positioning && (
            <Card title="竞争定位" style={{ marginBottom: 16 }}>
              <ReactMarkdown>{state.competitive_positioning}</ReactMarkdown>
            </Card>
          )}
          <Collapse>
            {state.recommendations.map((rec, i) => (
              <Collapse.Panel header={`P${rec.priority} | ${rec.title} [${rec.category}]`} key={i}>
                <p><strong>描述:</strong> {rec.description}</p>
                <p><strong>依据:</strong> {rec.rationale}</p>
                <p><strong>投入:</strong> {rec.effort} | <strong>影响:</strong> {rec.impact} | <strong>周期:</strong> {rec.timeline}</p>
              </Collapse.Panel>
            ))}
          </Collapse>
        </div>
      ),
    },
    {
      key: '6',
      label: '⚠️ 风险评估',
      children: (
        <Card>
          <ReactMarkdown>{state.risk_assessment || '未生成风险评估'}</ReactMarkdown>
        </Card>
      ),
    },
    {
      key: '7',
      label: '📝 日志',
      children: (
        <Card>
          {state.errors.length > 0 && (
            <Alert message="Errors" description={<ul>{state.errors.map((e, i) => <li key={i}>{e}</li>)}</ul>} type="error" showIcon style={{ marginBottom: 16 }} />
          )}
          <pre style={{ maxHeight: '400px', overflowY: 'auto', background: '#f5f5f5', padding: '16px' }}>
            {state.agent_logs.join('\n')}
          </pre>
        </Card>
      ),
    },
  ];

  return (
    <div>
      {state.executive_summary && (
        <Alert
          message="Executive Summary"
          description={<ReactMarkdown>{state.executive_summary}</ReactMarkdown>}
          type="info"
          showIcon
          style={{ marginBottom: 24 }}
        />
      )}
      <Tabs items={items} />
    </div>
  );
};
