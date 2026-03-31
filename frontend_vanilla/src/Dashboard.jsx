import { useInference } from './hooks/useInference';
import { Link } from 'react-router-dom';

/**
 * RoadSight Precision | Dashboard Refined
 * Recreated Production Dashboard (Stitch Design)
 * Data-wired to live FastAPI backend at http://localhost:8000
 */
const Dashboard = () => {
  const {
    image,
    loading,
    result,
    error,
    apiOnline,
    history,
    handleImageUpload,
    handleFileDrop,
    runAnalysis,
  } = useInference();

  // ── Metric card counts derived from localStorage history ──────────────────
  const totalScanned  = history.length;
  const potholeCount  = history.filter(h => h.result?.prediction?.class === 'Pothole').length;
  const crackCount    = history.filter(h => h.result?.prediction?.class === 'Crack').length;
  const normalCount   = history.filter(h => h.result?.prediction?.class === 'Normal').length;

  // ── Map API result fields to display values ────────────────────────────────
  const predClass      = result?.prediction?.class      ?? null;
  const confPct        = result?.prediction?.confidence != null
    ? (result.prediction.confidence * 100).toFixed(1)
    : null;
  const allConf        = result?.prediction?.all_confidences ?? {};
  const coverage       = result?.segmentation?.coverage_percent ?? {};
  const rpsScore       = result?.repair_priority?.score      ?? null;
  const severity       = result?.repair_priority?.severity   ?? null;
  const recommendation = result?.repair_priority?.recommendation ?? null;

  // Severity → badge color mapping
  const severityColor = {
    High:   'bg-pothole-red',
    Medium: 'bg-amber-500',
    Low:    'bg-normal-green',
  }[severity] ?? 'bg-pothole-red';

  // Confidence bars: Pothole → Crack → Normal
  const confidenceBars = [
    { label: 'Pothole Signature',  key: 'Pothole', color: 'bg-pothole-red',  text: 'text-pothole-red' },
    { label: 'Structural Fissure', key: 'Crack',   color: 'bg-amber-500',    text: 'text-amber-600'   },
    { label: 'Baseline Pavement',  key: 'Normal',  color: 'bg-normal-green', text: 'text-normal-green' },
  ];

  // Coverage grid cells: Background, Hairline Crack, Alligator Crack, Deep Pothole
  const coverageItems = [
    { label: 'Background',      key: 'Background',      color: 'bg-zinc-100'        },
    { label: 'Hairline Crack',  key: 'Hairline Crack',  color: 'bg-amber-300/60'    },
    { label: 'Alligator Crack', key: 'Alligator Crack', color: 'bg-pothole-red/60'  },
    { label: 'Deep Pothole',    key: 'Deep Pothole',    color: 'bg-pothole-red/90'  },
  ];

  // ── History table rows (latest 10 shown) ──────────────────────────────────
  const historyRows = history.slice(0, 10).map((h) => {
    const cls = h.result?.prediction?.class ?? 'Unknown';
    const conf = h.result?.prediction?.confidence != null
      ? Math.round(h.result.prediction.confidence * 100)
      : 0;
    const statusMap = { Pothole: 'Critical', Crack: 'Warning', Normal: 'Clear' };
    const colorMap  = {
      Pothole: { color: 'text-pothole-red', bg: 'bg-pothole-red', border: 'border-pothole-red' },
      Crack:   { color: 'text-amber-600',   bg: 'bg-amber-500',   border: 'border-amber-500'   },
      Normal:  { color: 'text-normal-green', bg: 'bg-normal-green', border: 'border-normal-green' },
    };
    const colors = colorMap[cls] ?? colorMap.Normal;
    return {
      id:         h.id,
      entity:     h.filename,
      time:       new Date(h.timestamp).toLocaleString(),
      result:     cls,
      confidence: conf,
      status:     statusMap[cls] ?? cls,
      ...colors,
    };
  });

  // Fall back to static placeholder rows when history is empty
  const staticScans = [
    { id: 'IMG_8422', entity: 'IMG_8422_POTHOLE.jpg', time: '2023-10-24 14:22:05', result: 'Pothole', confidence: 98, status: 'Critical', color: 'text-pothole-red', bg: 'bg-pothole-red', border: 'border-pothole-red' },
    { id: 'IMG_8421', entity: 'IMG_8421_CRACK.jpg',   time: '2023-10-24 14:15:32', result: 'Crack',   confidence: 74, status: 'Warning',  color: 'text-amber-600',   bg: 'bg-amber-500',   border: 'border-amber-500'   },
    { id: 'IMG_8420', entity: 'IMG_8420_NORMAL.jpg',  time: '2023-10-24 14:02:11', result: 'Normal',  confidence: 99, status: 'Clear',    color: 'text-normal-green', bg: 'bg-normal-green', border: 'border-normal-green' },
  ];

  const tableRows = historyRows.length > 0 ? historyRows : staticScans;

  // ── Drag-and-drop handlers ─────────────────────────────────────────────────
  const onDragOver  = (e) => e.preventDefault();
  const onDrop = (e) => {
    e.preventDefault();
    const f = e.dataTransfer.files?.[0];
    if (f && f.type.startsWith('image/')) {
      // reuse the hook's file-drop handler
      handleFileDrop(f);
    }
  };

  return (
    <div className="flex bg-surface font-headline text-on-surface antialiased digital-grid min-h-screen">
      <style>{`
        .digital-grid {
          background-image: radial-gradient(circle, #e1e3e4 1px, transparent 1px);
          background-size: 24px 24px;
        }
        .thin-border { border: 1px solid rgba(0,0,0,0.05); }
      `}</style>

      {/* SideNavBar Component */}
      <aside className="w-64 fixed left-0 top-0 h-full z-50 bg-[#f3f4f5] border-r border-black/5 flex flex-col py-8 shadow-sm">
        <div className="px-6 mb-10">
          <h1 className="text-on-surface font-black uppercase text-[0.6875rem] tracking-[0.1em]">Modern Precision</h1>
          <p className="text-[10px] text-zinc-500 font-bold mt-1 opacity-70">Digital Surveyor v2.1</p>
        </div>
        
        <nav className="flex flex-col space-y-1.5 px-3">
          <Link className="bg-gradient-to-br from-primary to-primary-container text-white rounded-xl px-4 py-3.5 shadow-md flex items-center gap-3 font-bold text-[0.8125rem] tracking-tight transition-transform active:scale-95" to="/dashboard">
            <span className="material-symbols-outlined text-[20px]">dashboard</span>
            Dashboard
          </Link>
          {[
            { name: 'Home', icon: 'home', path: '/' },
            { name: 'Analysis', icon: 'analytics', path: '/dashboard' },
            { name: 'History', icon: 'history', path: '/dashboard' },
            { name: 'Reports', icon: 'description', path: '/dashboard' }
          ].map((item) => (
            <Link key={item.name} className="text-on-surface-variant hover:bg-surface-variant/40 rounded-xl px-4 py-3.5 transition-all flex items-center gap-3 text-[0.8125rem] font-bold group hover:translate-x-1 duration-300" to={item.path}>
              <span className="material-symbols-outlined text-[20px] opacity-50 group-hover:opacity-100">{item.icon}</span>
              {item.name}
            </Link>
          ))}
        </nav>

        <div className="mt-auto px-3 space-y-1.5 border-t border-black/5 pt-6">
          <a className="text-on-surface-variant hover:bg-surface-variant/40 rounded-xl px-4 py-3 flex items-center gap-3 text-[0.8125rem] font-bold group" href="#">
            <span className="material-symbols-outlined text-[18px] opacity-50 group-hover:opacity-100">help</span>
            Support Center
          </a>
          <div className="flex items-center gap-3 px-4 py-5 bg-surface-container rounded-2xl mt-4 border border-black/5">
            <div className="w-10 h-10 rounded-xl bg-primary text-white flex items-center justify-center font-black text-xs shadow-inner">JD</div>
            <div className="overflow-hidden">
              <p className="text-[12px] font-black tracking-tight truncate">John Doe</p>
              <p className="text-[10px] text-zinc-500 font-bold truncate opacity-80 uppercase tracking-widest">Administrator</p>
            </div>
          </div>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="ml-64 flex-1 flex flex-col min-w-0">
        {/* TopAppBar Component */}
        <header className="sticky top-0 w-full z-40 bg-surface/80 backdrop-blur-xl border-b border-black/5 h-16 flex items-center justify-between px-10 shadow-sm">
          <div className="flex items-center gap-4">
            <span className="text-[11px] font-black text-zinc-400 uppercase tracking-widest">Infrastructure Analytics / Overview</span>
          </div>
          <div className="flex items-center gap-6">
            {/* Live API status badge — updated every 30 s via healthCheck() */}
            <span className={`text-[10px] font-black flex items-center gap-2 px-4 py-1.5 rounded-full border uppercase tracking-widest transition-all ${
              apiOnline
                ? 'text-normal-green bg-normal-green/5 border-normal-green/10'
                : 'text-pothole-red bg-pothole-red/5 border-pothole-red/10'
            }`}>
              <span className={`w-2 h-2 rounded-full animate-pulse ${apiOnline ? 'bg-normal-green' : 'bg-pothole-red'}`}></span>
              Neural Engine: {apiOnline ? 'Healthy' : 'Offline'}
            </span>
            <div className="flex items-center gap-2">
              <button className="w-10 h-10 flex items-center justify-center rounded-xl hover:bg-surface-container transition-all material-symbols-outlined text-zinc-400 hover:text-primary">api</button>
              <button className="w-10 h-10 flex items-center justify-center rounded-xl hover:bg-surface-container transition-all material-symbols-outlined text-zinc-400 hover:text-primary">notifications</button>
              <button className="w-10 h-10 flex items-center justify-center rounded-xl hover:bg-surface-container transition-all material-symbols-outlined text-zinc-400 hover:text-primary">settings</button>
            </div>
          </div>
        </header>

        {/* Canvas */}
        <div className="p-10 max-w-7xl mx-auto w-full space-y-10">
          {/* Metric Cards Row — counts from localStorage history */}
          <section className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {[
              { label: 'Total Scanned',  value: totalScanned,  grow: '+Latest',      color: 'primary',       border: 'border-l-primary',       icon: 'analytics'      },
              { label: 'Potholes Found', value: potholeCount,  grow: 'High Alert',   color: 'pothole-red',   border: 'border-l-pothole-red',   icon: 'report_problem' },
              { label: 'Cracks Found',   value: crackCount,    grow: 'Review Needs', color: 'amber-500',     border: 'border-l-amber-500',     icon: 'construction'   },
              { label: 'Normal Roads',   value: normalCount,   grow: 'Stable',       color: 'normal-green',  border: 'border-l-normal-green',  icon: 'verified'       }
            ].map((metric) => (
              <div key={metric.label} className={`bg-surface-container-lowest thin-border rounded-2xl p-7 flex flex-col justify-between shadow-sm border-l-8 ${metric.border}`}>
                <div className="flex justify-between items-start mb-8">
                  <span className="text-[10px] font-black text-zinc-400 tracking-[0.15em] uppercase">{metric.label}</span>
                  <span className={`material-symbols-outlined text-${metric.color} text-xl opacity-60`}>{metric.icon}</span>
                </div>
                <div>
                  <h2 className="text-4xl font-black tracking-tighter text-on-surface">{metric.value}</h2>
                  <p className={`text-[11px] font-black text-${metric.color} mt-2 uppercase tracking-widest`}>{metric.grow}</p>
                </div>
              </div>
            ))}
          </section>

          {/* Main Analysis Grid */}
          <section className="grid grid-cols-1 xl:grid-cols-2 gap-10">
            {/* Left: Ingestion Engine */}
            <div className="bg-surface-container-lowest thin-border rounded-2xl p-10 flex flex-col gap-10 shadow-sm relative overflow-hidden group">
              <div className="absolute top-0 right-0 p-10 opacity-5 group-hover:opacity-10 transition-opacity">
                <span className="material-symbols-outlined text-9xl">memory</span>
              </div>
              <div className="flex items-center justify-between relative z-10">
                <h3 className="text-[11px] font-black text-on-surface uppercase tracking-[0.2em]">Neural Ingestion Engine</h3>
                <button className="text-[10px] font-black text-primary hover:opacity-80 flex items-center gap-2 uppercase tracking-widest border-b border-primary/20">Protocol Specs</button>
              </div>
              
              <div className="flex-1 flex flex-col gap-10 relative z-10">
                {/* Drag & Drop Zone */}
                <label
                  className="border-2 border-dashed border-zinc-200 rounded-2xl p-12 flex flex-col items-center justify-center gap-6 bg-surface hover:bg-white hover:border-primary/40 transition-all cursor-pointer group/upload"
                  onDragOver={onDragOver}
                  onDrop={onDrop}
                >
                  <div className="w-16 h-16 rounded-2xl bg-primary/5 flex items-center justify-center text-primary group-hover/upload:bg-primary group-hover/upload:text-white transition-all shadow-sm">
                    <span className="material-symbols-outlined text-3xl">upload_file</span>
                  </div>
                  <div className="text-center">
                    <p className="text-[0.9375rem] font-black tracking-tight">Deploy new survey frame or <span className="text-primary underline underline-offset-4">browse filesystem</span></p>
                    <p className="text-[11px] text-zinc-400 mt-2 font-bold uppercase tracking-[0.1em]">Supported: NV12, RAW, RGB High Latency (Max 50MB)</p>
                  </div>
                  <input type="file" className="hidden" onChange={handleImageUpload} accept="image/*" />
                </label>

                {/* Latest Frame Preview */}
                <div className="flex flex-col gap-6">
                  <span className="text-[10px] font-black text-zinc-400 uppercase tracking-widest flex items-center gap-3">
                    <span className="w-2 h-2 bg-primary rounded-full animate-pulse"></span>
                    Live Inspection Monitor
                  </span>
                  <div className="relative rounded-2xl overflow-hidden h-60 group shadow-2xl border border-black/5 bg-zinc-900">
                    {image ? (
                      <img alt="Analysis Preview" className="w-full h-full object-cover grayscale-[30%] group-hover:grayscale-0 transition-transform duration-1000 group-hover:scale-105" src={image} />
                    ) : (
                      <div className="w-full h-full flex flex-col items-center justify-center opacity-30 gap-4">
                        <span className="material-symbols-outlined text-5xl text-white">satellite_alt</span>
                        <span className="text-[10px] font-bold text-white uppercase tracking-widest">Waiting for Data Ingestion...</span>
                      </div>
                    )}
                    <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-black/20 to-transparent flex flex-col justify-end p-8">
                      <div className="flex items-center justify-between text-white">
                        <div className="flex flex-col">
                          <p className="text-[10px] font-black opacity-60 uppercase tracking-widest mb-1">Source Pipeline</p>
                          <p className="text-sm font-black tracking-tight">{image ? 'EXTERNAL_SURVEY_01.jpg' : '0.0.0.0:8000/stream'}</p>
                        </div>
                        {image && (
                          <span className="text-[10px] bg-pothole-red text-white px-4 py-1.5 rounded-lg font-black tracking-widest shadow-lg animate-fade-in group-hover:scale-110 transition-transform">TARGET IDENTIFIED</span>
                        )}
                      </div>
                    </div>
                  </div>
                </div>

                {/* Error box */}
                {error && (
                  <div className="flex items-start gap-3 px-6 py-4 bg-pothole-red/10 border border-pothole-red/20 rounded-2xl">
                    <span className="material-symbols-outlined text-pothole-red text-lg mt-0.5">error</span>
                    <p className="text-[12px] font-black text-pothole-red tracking-tight">{error}</p>
                  </div>
                )}

                <button 
                  onClick={runAnalysis}
                  className={`w-full py-5 rounded-2xl font-black text-sm uppercase tracking-widest transition-all shadow-xl active:scale-95 ${loading ? 'bg-zinc-200 text-zinc-500 cursor-wait' : 'bg-primary text-white hover:bg-primary-container'}`}
                  disabled={loading || !image}
                >
                  {loading ? 'Executing Neural Logic...' : 'Run Diagnostics'}
                </button>
              </div>
            </div>

            {/* Right: Detection Result Detail */}
            <div className="bg-surface-container-lowest thin-border rounded-2xl p-10 flex flex-col gap-10 shadow-sm border-t-8 border-t-pothole-red relative overflow-hidden">
               <div className="absolute top-0 right-0 p-12 opacity-5">
                  <span className="material-symbols-outlined text-[200px] text-pothole-red">warning</span>
               </div>

              <div className="flex items-start justify-between relative z-10">
                <div>
                  <h3 className="text-[11px] font-black text-on-surface uppercase tracking-[0.2em]">Inference Analytics</h3>
                  <p className="text-[10px] text-zinc-500 font-bold mt-1 uppercase tracking-widest opacity-70">Tensor Processing Latency: 42ms</p>
                </div>
                <span className={`${result ? severityColor : 'bg-pothole-red'} text-white px-5 py-2 rounded-xl text-[10px] font-black tracking-widest flex items-center gap-3 shadow-lg group`}>
                  <span className="w-2.5 h-2.5 rounded-full bg-white animate-ping"></span>
                  {result ? (predClass?.toUpperCase() ?? 'ANALYSED') : 'SYSTEM IDLE'}
                </span>
              </div>

              {/* Prediction Metadata */}
              <div className="grid grid-cols-2 gap-6 relative z-10">
                <div className="bg-pothole-red/5 p-6 rounded-2xl border border-pothole-red/10 group hover:bg-pothole-red/10 transition-colors">
                  <p className="text-[10px] font-black text-pothole-red/60 uppercase mb-4 tracking-widest">Hazard Severity Index</p>
                  <div className="flex items-center gap-3">
                    <span className="material-symbols-outlined text-pothole-red text-3xl" style={{ fontVariationSettings: "'FILL' 1" }}>priority_high</span>
                    <span className="text-3xl font-black text-pothole-red tracking-tighter">
                      {severity?.toUpperCase() ?? 'CRITICAL'}
                    </span>
                  </div>
                </div>
                <div className="bg-surface-container-low p-6 rounded-2xl border border-black/5 group hover:bg-surface-container transition-colors">
                  <p className="text-[10px] font-black text-zinc-400 uppercase mb-4 tracking-widest">Maintenance Priority</p>
                  <div className="flex items-center gap-3">
                    <span className="material-symbols-outlined text-zinc-900 text-3xl">precision_manufacturing</span>
                    <span className="text-3xl font-black text-zinc-900 tracking-tighter">
                      {rpsScore != null ? rpsScore.toFixed(2) : '—'}
                      <span className="text-xs font-bold text-zinc-400 uppercase ml-1">Score</span>
                    </span>
                  </div>
                  {/* RPS progress bar */}
                  {rpsScore != null && (
                    <div className="mt-4 h-2 w-full bg-surface-container rounded-full overflow-hidden">
                      <div
                        className="h-full bg-pothole-red rounded-full transition-all duration-1000 ease-out"
                        style={{ width: `${Math.min(rpsScore / 5 * 100, 100)}%` }}
                      />
                    </div>
                  )}
                </div>
              </div>

              {/* Confidence Bars */}
              <div className="space-y-6 relative z-10">
                <p className="text-[10px] font-black text-zinc-400 uppercase tracking-widest flex justify-between">
                  <span>Classification Confidence Matrix</span>
                  <span className="text-primary font-bold">Neural Verifier v4.2</span>
                </p>
                <div className="space-y-5">
                  {confidenceBars.map((row) => {
                    const rawVal = allConf[row.key];
                    const val = rawVal != null ? parseFloat((rawVal * 100).toFixed(1)) : 0;
                    return (
                      <div key={row.label} className="space-y-2">
                        <div className="flex justify-between text-[11px] font-black uppercase tracking-tight">
                          <span className="text-on-surface">{row.label}</span>
                          <span className={row.text}>{val}%</span>
                        </div>
                        <div className="h-2.5 w-full bg-surface-container rounded-full overflow-hidden shadow-inner">
                          <div className={`h-full ${row.color} rounded-full transition-all duration-1000 ease-out shadow-[0px_0px_12px_rgba(0,0,0,0.1)]`} style={{ width: `${val}%` }}></div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Details & Coverage Grid */}
              <div className="flex gap-8 mt-4 pt-10 border-t border-black/5 relative z-10">
                <div className="w-1/3">
                  <p className="text-[10px] font-black text-zinc-400 uppercase mb-5 tracking-widest">Defect Density Mask</p>
                  <div className="grid grid-cols-2 gap-2 h-24">
                    {coverageItems.map((cell) => {
                      const pct = coverage[cell.key];
                      return (
                        <div
                          key={cell.key}
                          title={`${cell.label}: ${pct != null ? pct.toFixed(1) + '%' : '—'}`}
                          className={`${cell.color} rounded-lg cursor-help transition-colors shadow-sm hover:opacity-80 flex items-end p-1`}
                        >
                          {pct != null && (
                            <span className="text-[8px] font-black text-white/80 leading-none">{pct.toFixed(0)}%</span>
                          )}
                        </div>
                      );
                    })}
                  </div>
                </div>
                <div className="flex-1 bg-[#191c1d] p-7 border-l-8 border-pothole-red rounded-2xl shadow-2xl">
                  <div className="flex items-center gap-3 mb-3">
                    <span className="material-symbols-outlined text-pothole-red text-sm">psychology</span>
                    <p className="text-[11px] font-black text-white uppercase tracking-widest">Automated Action Plan</p>
                  </div>
                  <p className="text-[11px] leading-relaxed text-zinc-400 font-bold italic tracking-tight">
                    {recommendation
                      ? `"${recommendation}"`
                      : '"Structural depth exceeds 15cm threshold. High probability of tire delamination for high-speed transit. Deploying asphalt patching unit [CODE_RED] within 24hr survey window."'
                    }
                  </p>
                </div>
              </div>
            </div>
          </section>

          {/* Global Scan Registry Table */}
          <section className="bg-surface-container-lowest thin-border rounded-2xl overflow-hidden shadow-2xl border-b-2 border-b-primary/10">
            <div className="px-10 py-8 border-b border-black/5 flex items-center justify-between bg-white relative overflow-hidden">
               <div className="absolute inset-0 opacity-[0.03] pointer-events-none digital-grid"></div>
              <h3 className="text-[11px] font-black text-on-surface uppercase tracking-[0.2em] relative z-10">Master Civil Infrastructure Registry</h3>
              <div className="flex items-center gap-4 relative z-10">
                <button className="px-6 py-2.5 text-[10px] font-black text-zinc-500 hover:text-on-surface transition-all border border-zinc-200 rounded-xl uppercase tracking-widest hover:border-zinc-900 active:scale-95">Dataset v3 Export</button>
                <button className="px-6 py-2.5 text-[10px] font-black bg-zinc-900 text-white rounded-xl hover:bg-black transition-all uppercase tracking-widest shadow-lg shadow-black/10 active:scale-95">Batch Certification</button>
              </div>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="bg-surface-container-low/50 border-b border-black/5">
                    <th className="px-10 py-6 text-[10px] font-black text-zinc-400 uppercase tracking-[0.2em]">Risk Grading</th>
                    <th className="px-10 py-6 text-[10px] font-black text-zinc-400 uppercase tracking-[0.2em]">Entity Signature</th>
                    <th className="px-10 py-6 text-[10px] font-black text-zinc-400 uppercase tracking-[0.2em]">Temporal Stamp</th>
                    <th className="px-10 py-6 text-[10px] font-black text-zinc-400 uppercase tracking-[0.2em]">Inference Verdict</th>
                    <th className="px-10 py-6 text-[10px] font-black text-zinc-400 uppercase tracking-[0.2em]">Confidence</th>
                    <th className="px-10 py-6 text-[10px] font-black text-zinc-400 uppercase tracking-[0.2em] text-right">Ops</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-black/5">
                  {tableRows.map((scan) => (
                    <tr key={scan.id} className="hover:bg-surface transition-all group duration-300">
                      <td className="px-10 py-6">
                        <div className="flex items-center gap-3">
                          <span className={`w-2.5 h-2.5 rounded-full ${scan.bg} shadow-md`}></span>
                          <span className={`text-[11px] font-black ${scan.color} uppercase tracking-widest`}>{scan.status}</span>
                        </div>
                      </td>
                      <td className="px-10 py-6 text-[0.8125rem] font-black text-on-surface tracking-tight group-hover:text-primary transition-colors">{scan.entity}</td>
                      <td className="px-10 py-6 text-[11px] text-zinc-500 font-bold font-mono tracking-widest opacity-80">{scan.time}</td>
                      <td className="px-10 py-6">
                        <span className={`${scan.bg}/5 ${scan.color} px-4 py-1.5 rounded-xl text-[10px] font-black border ${scan.border}/10 uppercase tracking-[0.15em] shadow-sm`}>
                          {scan.result}
                        </span>
                      </td>
                      <td className="px-10 py-6">
                        <div className="flex items-center gap-4">
                          <div className="w-24 h-2 bg-zinc-100 rounded-full overflow-hidden shadow-inner">
                            <div className={`h-full ${scan.bg} shadow-md`} style={{ width: `${scan.confidence}%` }}></div>
                          </div>
                          <span className="text-[11px] font-black text-zinc-900 font-mono italic">{scan.confidence}%</span>
                        </div>
                      </td>
                      <td className="px-10 py-6 text-right">
                        <button className="w-10 h-10 flex items-center justify-center rounded-xl material-symbols-outlined text-zinc-400 hover:bg-zinc-900 hover:text-white transition-all transform hover:rotate-12 duration-300 group-hover:scale-110 shadow-sm">visibility</button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        </div>

        {/* Dynamic Footer Info */}
        <footer className="mt-auto p-16 text-center">
          <div className="inline-flex items-center gap-5 bg-zinc-900/5 px-8 py-3 rounded-full border border-black/[0.03] backdrop-blur-sm group hover:bg-zinc-900/10 transition-colors cursor-default">
            <p className="text-[9px] text-zinc-500 font-black uppercase tracking-[0.3em] font-headline">Engineered for Public Infrastructure</p>
            <span className="w-1.5 h-1.5 bg-zinc-300 rounded-full animate-pulse group-hover:bg-primary"></span>
            <p className="text-[9px] text-zinc-500 font-black uppercase tracking-[0.3em] font-headline">v2.4.0 High-Precision Neural Core</p>
          </div>
        </footer>
      </main>
    </div>
  );
};

export default Dashboard;
