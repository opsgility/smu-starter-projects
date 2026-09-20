import { Inspection } from '@/types';

const SEVERITY_COLORS: Record<string, string> = {
  low: '#16A34A',
  medium: '#D97706',
  high: '#DC2626',
  critical: '#7C0A02',
};

const CONDITION_COLORS: Record<string, string> = {
  good: '#16A34A',
  fair: '#D97706',
  poor: '#DC2626',
  critical: '#7C0A02',
};

export function generateReportHtml(inspection: Inspection): string {
  const date = inspection.completedAt
    ? new Date(inspection.completedAt).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })
    : new Date(inspection.startedAt).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });

  const checkedCount = inspection.checklistItems.filter(c => c.checked).length;
  const totalItems = inspection.checklistItems.length;
  const highFindings = inspection.findings.filter(f => f.severity === 'high' || f.severity === 'critical');

  const findingsHtml = inspection.findings.length > 0
    ? inspection.findings.map(f => `
      <div style="margin-bottom: 12px; padding: 12px; border-left: 4px solid ${SEVERITY_COLORS[f.severity]}; background: #f9fafb; border-radius: 4px;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
          <strong style="font-size: 14px;">${f.title}</strong>
          <span style="font-size: 11px; font-weight: 700; color: ${SEVERITY_COLORS[f.severity]}; text-transform: uppercase;">${f.severity}</span>
        </div>
        ${f.description ? `<p style="margin: 0; font-size: 13px; color: #64748b;">${f.description}</p>` : ''}
      </div>`).join('')
    : '<p style="color: #94a3b8; font-size: 13px;">No findings recorded.</p>';

  const checklistHtml = inspection.checklistItems.length > 0
    ? inspection.checklistItems.map(c => `
      <div style="display: flex; align-items: center; padding: 6px 0; border-bottom: 1px solid #f1f5f9;">
        <span style="margin-right: 10px; font-size: 16px;">${c.checked ? '✅' : '⬜'}</span>
        <span style="font-size: 13px; color: ${c.checked ? '#0f172a' : '#94a3b8'}; ${c.checked ? '' : 'text-decoration: line-through'}">${c.label}</span>
        <span style="margin-left: auto; font-size: 11px; color: #94a3b8;">${c.category}</span>
      </div>`).join('')
    : '<p style="color: #94a3b8; font-size: 13px;">No checklist items.</p>';

  const aiAnalysisHtml = inspection.photos.filter(p => p.analysis).map(p => `
    <div style="margin-bottom: 12px; padding: 12px; background: #f8fafc; border-radius: 8px; border: 1px solid #e2e8f0;">
      <div style="display: flex; gap: 8px; margin-bottom: 8px;">
        <span style="font-size: 11px; font-weight: 700; padding: 2px 8px; border-radius: 4px; background: ${CONDITION_COLORS[p.analysis!.condition]}; color: white; text-transform: uppercase;">${p.analysis!.condition}</span>
        <span style="font-size: 11px; color: #64748b;">${new Date(p.takenAt).toLocaleTimeString()}</span>
      </div>
      <p style="margin: 0 0 6px; font-size: 13px;">${p.analysis!.summary}</p>
      ${p.analysis!.defects.length > 0 ? `<p style="margin: 0; font-size: 12px; color: #dc2626;"><strong>Defects:</strong> ${p.analysis!.defects.join(', ')}</p>` : ''}
    </div>`).join('');

  return `<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Inspection Report — ${inspection.equipmentName}</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; margin: 0; padding: 24px; color: #0f172a; background: #fff; }
    .header { border-bottom: 3px solid #1d4ed8; padding-bottom: 16px; margin-bottom: 24px; }
    .header h1 { margin: 0 0 4px; font-size: 22px; color: #1d4ed8; }
    .header .subtitle { margin: 0; font-size: 13px; color: #64748b; }
    .section { margin-bottom: 24px; }
    .section h2 { font-size: 14px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; color: #475569; border-bottom: 1px solid #e2e8f0; padding-bottom: 6px; margin-bottom: 12px; }
    .summary-grid { display: flex; gap: 16px; margin-bottom: 24px; }
    .summary-card { flex: 1; background: #f8fafc; border-radius: 8px; padding: 12px; text-align: center; border: 1px solid #e2e8f0; }
    .summary-card .num { font-size: 24px; font-weight: 700; color: #1d4ed8; }
    .summary-card .label { font-size: 11px; color: #64748b; margin-top: 2px; }
    .footer { margin-top: 40px; padding-top: 12px; border-top: 1px solid #e2e8f0; font-size: 11px; color: #94a3b8; text-align: center; }
  </style>
</head>
<body>
  <div class="header">
    <h1>Inspection Report</h1>
    <p class="subtitle">InspectAI · ${date}</p>
  </div>

  <div class="section">
    <h2>Equipment</h2>
    <p style="margin: 0; font-size: 16px; font-weight: 600;">${inspection.equipmentName}</p>
    <p style="margin: 4px 0 0; font-size: 13px; color: #64748b;">Status: <strong>${inspection.status === 'completed' ? 'Completed' : 'In Progress'}</strong></p>
  </div>

  <div class="summary-grid">
    <div class="summary-card">
      <div class="num">${inspection.photos.length}</div>
      <div class="label">Photos</div>
    </div>
    <div class="summary-card">
      <div class="num">${checkedCount}/${totalItems}</div>
      <div class="label">Checklist</div>
    </div>
    <div class="summary-card">
      <div class="num" style="color: ${inspection.findings.length > 0 ? (highFindings.length > 0 ? '#DC2626' : '#D97706') : '#16A34A'}">${inspection.findings.length}</div>
      <div class="label">Findings</div>
    </div>
  </div>

  <div class="section">
    <h2>Findings</h2>
    ${findingsHtml}
  </div>

  <div class="section">
    <h2>Checklist</h2>
    ${checklistHtml}
  </div>

  ${aiAnalysisHtml ? `<div class="section"><h2>AI Analysis</h2>${aiAnalysisHtml}</div>` : ''}

  <div class="footer">
    Generated by InspectAI · ${new Date().toLocaleString()}
  </div>
</body>
</html>`;
}
