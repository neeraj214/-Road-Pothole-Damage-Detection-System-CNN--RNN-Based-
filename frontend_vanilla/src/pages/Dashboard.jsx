import React from 'react';
import Sidebar from '../components/dashboard/Sidebar';
import MetricCards from '../components/dashboard/MetricCards';
import ScanRegistry from '../components/dashboard/ScanRegistry';
import { useInference } from '../hooks/useInference';
import { Search, Bell, Settings, Upload, FileText, Info, Loader2, AlertTriangle, LayoutDashboard } from 'lucide-react';

const Dashboard = () => {
  const inference = useInference();

  return (
    <div className="dashboard-layout digital-grid min-h-screen">
      <Sidebar />
      
      <main className="dashboard-main flex-1">
        <header className="dashboard-header glass sticky top-0 flex items-center justify-between px-8">
            <div className="breadcrumb flex items-center gap-4">
                <span className="text-xs font-bold text-on-surface-variant tracking-tight">Dashboard / Overview</span>
            </div>
            
            <div className="header-actions flex items-center gap-6">
                <div className="api-status flex items-center gap-1.5 px-3 py-1 bg-normal-green/10 rounded-full razor-border">
                    <span className="status-dot-pulse bg-normal-green"></span>
                    <span className="text-[10px] font-black uppercase text-normal-green">API Status: Healthy</span>
                </div>
                <div className="flex gap-2">
                    <button className="icon-btn-plain"><Bell size={18} /></button>
                    <button className="icon-btn-plain"><Settings size={18} /></button>
                </div>
            </div>
        </header>

        <div className="dashboard-scroll-content p-8 max-w-7xl mx-auto space-y-8">
            <MetricCards />

            <section className="analysis-grid mt-8">
                <div className="grid-2-col gap-8">
                    {/* Ingestion Engine Card */}
                    <div className="analysis-card surface-lowest razor-border p-8 flex flex-col gap-8 ghost-shadow">
                        <div className="flex items-center justify-between">
                            <h3 className="section-title">Ingestion Engine</h3>
                            <button className="text-[10px] font-black text-primary flex items-center gap-1 tracking-widest uppercase">
                                <Info size={12} /> Guidelines
                            </button>
                        </div>
                        
                        <div className="flex-1 flex flex-col gap-8">
                            <div className="drop-zone razor-border border-dashed hover-primary p-10 flex flex-col items-center justify-center gap-4 cursor-pointer relative overflow-hidden">
                                {inference.image ? (
                                    <div className="image-preview-full relative w-full h-full">
                                        <img src={inference.image} alt="Survey Input" className="preview-fit" />
                                        {inference.loading && (
                                            <div className="analyzing-overlay glass flex center flex-col">
                                                <Loader2 className="animate-spin mb-2" />
                                                <span className="text-[10px] font-black uppercase">Scanning</span>
                                            </div>
                                        )}
                                        {!inference.loading && (
                                            <button className="reset-btn-pill" onClick={inference.reset}>New Scan</button>
                                        )}
                                    </div>
                                ) : (
                                    <label className="flex flex-col items-center gap-3 cursor-pointer">
                                        <div className="icon-box-primary"><Upload size={24} /></div>
                                        <div className="text-center">
                                            <p className="text-sm font-bold">Deploy survey data or <span className="text-primary underline">browse</span></p>
                                            <p className="text-[10px] text-outline mt-1 font-medium italic">Supports RAW, JPG up to 50MB</p>
                                        </div>
                                        <input type="file" className="hidden" accept="image/*" onChange={(e) => inference.handleImageUpload(e.target.files[0])} />
                                    </label>
                                )}
                            </div>
                            
                            {!inference.result && (
                                <button className="btn-primary-large" onClick={inference.runAnalysis} disabled={!inference.image || inference.loading}>
                                    {inference.loading ? 'Executing Precision Inference...' : 'Run Analysis Engine'}
                                </button>
                            ) }
                        </div>
                    </div>

                    {/* Inference Detail Card */}
                    <div className="analysis-card surface-lowest razor-border p-8 flex flex-col gap-8 ghost-shadow">
                        <div className="flex items-start justify-between">
                            <div>
                                <h3 className="section-title">Inference Analytics</h3>
                                <p className="text-[10px] font-medium text-outline">Model precision latency: 1.2s</p>
                            </div>
                            {inference.result && (
                                <div className="hazard-pill flex items-center gap-2">
                                    <div className="pulse-white-dot"></div>
                                    <span className="text-[9px] font-black tracking-widest uppercase">{inference.result.hazard_type} Detected</span>
                                </div>
                            )}
                        </div>

                        {inference.result ? (
                            <div className="inference-details space-y-8 fade-in">
                                <div className="grid grid-2 gap-4">
                                    <div className="detail-stat-box status-error">
                                        <p className="label-sm opacity-70 mb-2">Severity Index</p>
                                        <div className="flex items-center gap-2">
                                            <AlertTriangle size={20} />
                                            <span className="text-xl font-black">{inference.result.severity.toUpperCase()}</span>
                                        </div>
                                    </div>
                                    <div className="detail-stat-box status-neutral">
                                        <p className="label-sm opacity-70 mb-2">Repair Priority</p>
                                        <div className="flex items-center gap-2">
                                            <FileText size={20} />
                                            <span className="text-xl font-black">92 / 100</span>
                                        </div>
                                    </div>
                                </div>

                                <div className="confidence-stack space-y-4">
                                    <p className="label-sm text-outline tracking-widest uppercase">Classification Confidence</p>
                                    <div className="confidence-item space-y-1.5">
                                        <div className="flex justify-between text-[11px] font-bold">
                                            <span>{inference.result.hazard_type} Neural Matrix</span>
                                            <span className="text-pothole-red">{(inference.result.confidence * 100).toFixed(1)}%</span>
                                        </div>
                                        <div className="bar-base">
                                            <div className="bar-fill" style={{ width: `${inference.result.confidence * 100}%`, backgroundColor: 'var(--pothole-red)' }}></div>
                                        </div>
                                    </div>
                                    <div className="confidence-item opacity-40 space-y-1.5">
                                        <div className="flex justify-between text-[11px] font-bold">
                                            <span>Baseline Road Structural</span>
                                            <span>0.4%</span>
                                        </div>
                                        <div className="bar-base">
                                            <div className="bar-fill" style={{ width: '0.4%', backgroundColor: 'var(--normal-green)' }}></div>
                                        </div>
                                    </div>
                                </div>

                                <div className="recommendation-area p-5 border-l-4 border-pothole-red surface-low rounded-r-lg">
                                    <p className="text-[11px] font-black mb-2 uppercase">AI Recommendation</p>
                                    <p className="text-[11px] leading-relaxed italic text-on-surface-variant">
                                        "Immediate asphalt patching required. Damage exceeds threshold. High risk of vehicle tire failure on this segment survey."
                                    </p>
                                </div>
                            </div>
                        ) : (
                            <div className="flex-1 flex flex-col items-center justify-center text-center px-12 opacity-30">
                                <LayoutDashboard size={48} className="mb-4" />
                                <p className="text-sm font-bold">Inference Analytics Idle</p>
                                <p className="text-xs font-medium mt-1">Deploy survey frame to begin real-time neural mapping.</p>
                            </div>
                        )}
                    </div>
                </div>
            </section>

            <ScanRegistry />
        </div>

        <footer className="dashboard-footer p-8 text-center mt-auto">
             <div className="inline-flex items-center gap-4 bg-zinc-900/5 px-6 py-2 rounded-full razor-border">
                <p className="text-[9px] text-zinc-400 font-bold uppercase tracking-[0.2em]">v2.4.0 High Precision Neural Network</p>
             </div>
        </footer>
      </main>

      <style dangerouslySetInnerHTML={{ __html: `
        .dashboard-layout { display: flex; }
        .dashboard-main { 
            margin-left: 256px; 
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
        .dashboard-header { height: 64px; border-bottom: 1px solid var(--outline-variant); }
        .section-title { font-size: 0.6875rem; font-weight: 900; text-transform: uppercase; letter-spacing: 0.1em; color: var(--on-surface); }
        .status-dot-pulse { width: 6px; height: 6px; border-radius: 50%; display: inline-block; animation: pulse-green 2s infinite; }
        @keyframes pulse-green { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
        
        .grid-2-col { display: grid; grid-template-columns: 1fr 1fr; gap: var(--spacing-8); }
        .analysis-card { border-radius: var(--radius-xl); min-height: 480px; }
        
        .drop-zone { height: 260px; border-radius: var(--radius-lg); background-color: var(--surface); transition: 0.2s; }
        .drop-zone.hover-primary:hover { border-color: var(--primary); }
        .icon-box-primary { width: 48px; height: 48px; background: var(--primary-container); color: var(--primary); border-radius: var(--radius-md); display: flex; items-center justify-center; }
        
        .image-preview-full { border-radius: var(--radius-md); overflow: hidden; }
        .preview-fit { width: 100%; height: 100%; object-fit: cover; }
        .reset-btn-pill { position: absolute; bottom: 12px; right: 12px; background: white; border: none; padding: 0.5rem 1rem; border-radius: var(--radius-full); font-size: 10px; font-weight: 900; text-transform: uppercase; box-shadow: var(--shadow-ghost); cursor: pointer; }
        
        .btn-primary-large {
            padding: 1.25rem; background: var(--primary); color: white; border: none; border-radius: var(--radius-md); font-weight: 700; font-size: 0.875rem; cursor: pointer; transition: 0.2s;
        }
        .btn-primary-large:hover:not(:disabled) { opacity: 0.9; }
        .btn-primary-large:disabled { opacity: 0.5; }
        
        .hazard-pill { background-color: var(--pothole-red); color: white; padding: 0.5rem 1rem; border-radius: var(--radius-md); }
        .pulse-white-dot { width: 6px; height: 6px; background: white; border-radius: 50%; filter: blur(1px); animation: pulse-white 2s infinite; }
        @keyframes pulse-white { 0%, 100% { opacity: 1; transform: scale(1); } 50% { opacity: 0.5; transform: scale(1.2); } }
        
        .detail-stat-box { padding: 1.25rem; border-radius: var(--radius-lg); border: 1px solid var(--outline-variant); }
        .detail-stat-box.status-error { background-color: #fdf3f3; color: var(--pothole-red); border-color: rgba(186, 26, 26, 0.1); }
        .detail-stat-box.status-neutral { background-color: var(--surface-low); color: var(--on-surface); }
        
        .bar-base { height: 8px; width: 100%; background: var(--surface-container); border-radius: var(--radius-full); overflow: hidden; }
        .bar-fill { height: 100%; border-radius: var(--radius-full); }
        
        .center { display: flex; align-items: center; justify-content: center; }
        .icon-btn-plain { background: none; border: none; color: var(--outline); padding: 8px; cursor: pointer; border-radius: var(--radius-md); }
        .icon-btn-plain:hover { background-color: var(--surface-container); color: var(--on-surface); }
      `}} />
    </div>
  );
};

export default Dashboard;
