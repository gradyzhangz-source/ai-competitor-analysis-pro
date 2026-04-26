import React, { useState, useRef } from 'react';
import MDEditor from '@uiw/react-md-editor';
import { Button, Space, message } from 'antd';
import { DownloadOutlined, SaveOutlined } from '@ant-design/icons';
import html2pdf from 'html2pdf.js';

interface Props {
  initialValue: string;
  onSave?: (value: string) => void;
}

export const ReportEditor: React.FC<Props> = ({ initialValue, onSave }) => {
  const [value, setValue] = useState(initialValue);
  const printRef = useRef<HTMLDivElement>(null);

  const handleExportPDF = () => {
    if (!printRef.current) return;
    const element = printRef.current;
    const opt = {
      margin: 10,
      filename: '竞品分析报告.pdf',
      image: { type: 'jpeg', quality: 0.98 },
      html2canvas: { scale: 2, useCORS: true },
      jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
    };
    html2pdf().set(opt).from(element).save();
    message.success('正在导出 PDF...');
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
      <Space>
        <Button type="primary" icon={<SaveOutlined />} onClick={() => onSave?.(value)}>
          保存修改
        </Button>
        <Button icon={<DownloadOutlined />} onClick={handleExportPDF}>
          导出 PDF
        </Button>
      </Space>
      <div data-color-mode="light">
        <MDEditor
          value={value}
          onChange={(val) => setValue(val || '')}
          height={600}
          preview="live"
        />
      </div>
      {/* Hidden div for PDF export */}
      <div style={{ display: 'none' }}>
        <div ref={printRef} style={{ padding: '20px', background: 'white', color: 'black' }}>
          <MDEditor.Markdown source={value} style={{ whiteSpace: 'pre-wrap' }} />
        </div>
      </div>
    </div>
  );
};
