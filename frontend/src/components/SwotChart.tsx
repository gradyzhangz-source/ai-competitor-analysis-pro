import React from 'react';
import { Card, Row, Col } from 'antd';

interface Props {
  data: any;
}

export const SwotChart: React.FC<Props> = ({ data }) => {
  if (!data) return <div>暂无数据</div>;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
      {data.map((swot: any) => (
        <Card key={swot.company} title={swot.company} size="small">
          <Row gutter={[16, 16]}>
            <Col span={12}>
              <Card title="💪 优势 (Strengths)" type="inner" headStyle={{ background: '#f6ffed' }}>
                <ul style={{ paddingLeft: 20 }}>{swot.strengths.map((s: string, i: number) => <li key={i}>{s}</li>)}</ul>
              </Card>
            </Col>
            <Col span={12}>
              <Card title="⚠️ 劣势 (Weaknesses)" type="inner" headStyle={{ background: '#fff2e8' }}>
                <ul style={{ paddingLeft: 20 }}>{swot.weaknesses.map((w: string, i: number) => <li key={i}>{w}</li>)}</ul>
              </Card>
            </Col>
            <Col span={12}>
              <Card title="🌟 机会 (Opportunities)" type="inner" headStyle={{ background: '#e6f7ff' }}>
                <ul style={{ paddingLeft: 20 }}>{swot.opportunities.map((o: string, i: number) => <li key={i}>{o}</li>)}</ul>
              </Card>
            </Col>
            <Col span={12}>
              <Card title="🔥 威胁 (Threats)" type="inner" headStyle={{ background: '#fff1f0' }}>
                <ul style={{ paddingLeft: 20 }}>{swot.threats.map((t: string, i: number) => <li key={i}>{t}</li>)}</ul>
              </Card>
            </Col>
          </Row>
        </Card>
      ))}
    </div>
  );
};
