import React from 'react';
import { Eye, Download, FileText } from 'lucide-react';

const ScanRegistry = () => {
  const scans = [
    { id: 'IMG_8422_POTHOLE.jpg', type: 'Pothole', severity: 'Critical', date: '2023-10-24 14:22:05', confidence: 0.98, color: 'var(--pothole-red)' },
    { id: 'IMG_8421_CRACK.jpg', type: 'Crack', severity: 'Warning', date: '2023-10-24 14:15:32', confidence: 0.74, color: 'var(--amber-warning)' },
    { id: 'IMG_8420_NORMAL.jpg', type: 'Normal', severity: 'Clear', date: '2023-10-24 14:02:11', confidence: 0.99, color: 'var(--normal-green)' }
  ];

  return (
    <div className="registry-container surface-lowest razor-border ghost-shadow overflow-hidden mt-8">
      <div className="px-8 py-6 border-bottom flex items-center justify-between">
        <h3 className="registry-title">Global Scan Registry</h3>
        <div className="flex items-center gap-3">
          <button className="btn-registry-outline"><Download size={14} /> Export Dataset</button>
          <button className="btn-registry-primary"><FileText size={14} /> Audit Report</button>
        </div>
      </div>
      
      <div className="overflow-x-auto">
        <table className="registry-table w-full">
          <thead>
            <tr className="surface-low border-bottom">
              <th>Status</th>
              <th>Entity ID</th>
              <th>Temporal Signature</th>
              <th>Inference Result</th>
              <th>Confidence</th>
              <th className="text-right">Ops</th>
            </tr>
          </thead>
          <tbody>
            {scans.map((scan, i) => (
              <tr key={i} className="registry-row">
                <td>
                  <div className="flex items-center gap-2">
                    <span className="status-indicator" style={{ backgroundColor: scan.color }}></span>
                    <span className="status-text font-bold uppercase tracking-wide" style={{ color: scan.color }}>{scan.severity}</span>
                  </div>
                </td>
                <td className="font-bold text-on-surface">{scan.id}</td>
                <td className="text-outline font-mono">{scan.date}</td>
                <td>
                  <span className="pill-small" style={{ backgroundColor: `${scan.color}10`, color: scan.color, borderColor: `${scan.color}20` }}>
                    {scan.type}
                  </span>
                </td>
                <td>
                  <div className="flex items-center gap-3">
                    <div className="progress-bar-small razor-border">
                        <div className="progress-fill" style={{ width: `${scan.confidence * 100}%`, backgroundColor: scan.color }}></div>
                    </div>
                    <span className="font-bold font-mono text-outline">{(scan.confidence * 100).toFixed(0)}%</span>
                  </div>
                </td>
                <td className="text-right">
                  <button className="view-btn"><Eye size={18} /></button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <style dangerouslySetInnerHTML={{ __html: `
        .registry-container { border-radius: var(--radius-xl); }
        .registry-title { font-size: 0.6875rem; font-weight: 900; text-transform: uppercase; letter-spacing: 0.1em; color: var(--on-surface); }
        .registry-table { border-collapse: collapse; text-align: left; }
        .registry-table th { padding: 1.25rem 2rem; font-size: 10px; font-weight: 900; text-transform: uppercase; letter-spacing: 0.15em; color: var(--outline); }
        .registry-table td { padding: 1.25rem 2rem; border-top: 1px solid var(--outline-variant); font-size: 13px; color: var(--on-surface-variant); }
        
        .registry-row:hover { background-color: var(--surface-container-low); }
        
        .status-indicator { width: 8px; height: 8px; border-radius: 50%; }
        .status-text { font-size: 11px; }
        
        .pill-small {
          display: inline-block;
          font-size: 10px;
          font-weight: 900;
          text-transform: uppercase;
          letter-spacing: 0.05em;
          padding: 0.25rem 0.625rem;
          border-radius: var(--radius-md);
          border: 1px solid;
        }
        
        .progress-bar-small { width: 80px; height: 6px; border-radius: var(--radius-full); background: var(--surface-container-low); overflow: hidden; }
        .progress-fill { height: 100%; border-radius: var(--radius-full); }
        
        .view-btn { background: none; border: none; padding: 4px; color: var(--outline); cursor: pointer; border-radius: var(--radius-md); }
        .view-btn:hover { background-color: var(--primary); color: white; }
        
        .btn-registry-outline, .btn-registry-primary {
          display: flex; align-items: center; gap: 0.5rem;
          font-size: 11px; font-weight: 900; text-transform: uppercase; letter-spacing: 0.05em;
          padding: 0.5rem 1rem; border-radius: var(--radius-md); cursor: pointer; transition: 0.2s;
        }
        .btn-registry-outline { background: white; border: 1px solid var(--outline-variant); color: var(--on-surface-variant); }
        .btn-registry-outline:hover { color: var(--on-surface); border-color: var(--outline); }
        .btn-registry-primary { background: var(--primary); color: white; border: none; box-shadow: var(--shadow-ghost); }
        .btn-registry-primary:hover { opacity: 0.9; }
      `}} />
    </div>
  );
};

export default ScanRegistry;
