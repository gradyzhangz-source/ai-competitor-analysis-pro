import React from 'react';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Tooltip } from 'recharts';

interface Props {
  data: any;
}

const parseLevel = (level: string) => {
  if (level.includes('高')) return 3;
  if (level.includes('中')) return 2;
  if (level.includes('低')) return 1;
  return 0;
};

export const PortersRadar: React.FC<Props> = ({ data }) => {
  if (!data) return <div>暂无数据</div>;

  const chartData = [
    { subject: '供应商议价能力', A: parseLevel(data.supplier_power?.level || '') },
    { subject: '买方议价能力', A: parseLevel(data.buyer_power?.level || '') },
    { subject: '行业竞争程度', A: parseLevel(data.competitive_rivalry?.level || '') },
    { subject: '替代品威胁', A: parseLevel(data.threat_of_substitution?.level || '') },
    { subject: '新进入者威胁', A: parseLevel(data.threat_of_new_entry?.level || '') },
  ];

  return (
    <div style={{ width: '100%', height: 400 }}>
      <ResponsiveContainer>
        <RadarChart cx="50%" cy="50%" outerRadius="80%" data={chartData}>
          <PolarGrid />
          <PolarAngleAxis dataKey="subject" />
          <PolarRadiusAxis angle={30} domain={[0, 3]} tick={false} />
          <Radar name="威胁等级 (3=高, 1=低)" dataKey="A" stroke="#8884d8" fill="#8884d8" fillOpacity={0.6} />
          <Tooltip />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
};
