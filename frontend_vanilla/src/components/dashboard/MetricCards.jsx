import React from 'react';
import { BarChart3, AlertTriangle, Hammer, CheckCircle } from 'lucide-react';

const MetricCards = () => {
  const metrics = [
    { label: 'Total Scanned', value: '1,284', change: '+12% from last week', color: 'var(--primary)', icon: <BarChart3 /> },
    { label: 'Potholes Found', value: '42', change: 'High Priority Action', color: 'var(--pothole-red)', icon: <AlertTriangle /> },
    { label: 'Cracks Found', value: '156', change: 'Needs Field Review', color: 'var(--amber-warning)', icon: <Hammer /> },
    { label: 'Normal Roads', value: '1,086', change: 'Structurally Stable', color: 'var(--normal-green)', icon: <CheckCircle /> }
  ];

  return (
    <div className="metrics-grid">
      {metrics.map((m, i) => (
        <div key={i} className="metric-card surface-lowest razor-border ghost-shadow" style={{ borderLeft: `6px solid ${m.color}` }}>
          <div className="flex justify-between items-start mb-6">
            <span className="metric-label label-sm text-outline">{m.label}</span>
            <div style={{ color: m.color, opacity: 0.4 }}>{m.icon}</div>
          </div>
          <div>
            <h2 className="metric-value">{m.value}</h2>
            <p className="metric-change" style={{ color: m.color }}>{m.change}</p>
          </div>
        </div>
      ))}

      <style dangerouslySetInnerHTML={{ __html: `
        .metrics-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
          gap: var(--spacing-6);
        }
        .metric-card {
          padding: 1.5rem;
          border-radius: var(--radius-lg);
          display: flex;
          flex-direction: column;
          justify-content: space-between;
        }
        .metric-value {
          font-size: 2.25rem;
          font-weight: 900;
          letter-spacing: -0.05em;
          color: var(--on-surface);
        }
        .metric-change {
          font-size: 12px;
          font-weight: 700;
          margin-top: 0.25rem;
        }
      `}} />
    </div>
  );
};

export default MetricCards;
