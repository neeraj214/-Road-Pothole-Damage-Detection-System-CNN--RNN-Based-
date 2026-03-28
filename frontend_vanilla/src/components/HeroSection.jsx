import React from 'react';
import { Play, FileText, Upload, Loader2, CheckCircle2, AlertCircle } from 'lucide-react';

const HeroSection = ({ 
  image, 
  loading, 
  result, 
  error, 
  onUpload, 
  onAnalyze, 
  onReset 
}) => {
  return (
    <section className="hero-section flex items-center overflow-hidden">
      <div className="hero-background">
        <img 
          src="https://images.unsplash.com/photo-1545143333-7e82f24c62a7?q=80&w=2560&auto=format&fit=crop" 
          alt="Modern highway" 
          className="hero-image"
        />
        <div className="hero-overlay"></div>
      </div>
      
      <div className="container relative z-10 flex hero-content-grid">
        <div className="max-w-xl hero-text fade-in">
          <span className="label-pill label-sm mb-6">Infrastructure Intelligence</span>
          <h1 className="hero-title white mb-8">
            The Future of <br/>
            <span className="text-accent">Digital Surveying.</span>
          </h1>
          <p className="hero-description mb-10">
            Harness the power of high-precision AI to monitor, detect, and prioritize road maintenance with surgical accuracy.
          </p>
          
          <div className="flex gap-4">
            <button className="btn-primary" onClick={onAnalyze} disabled={loading || !image}>
              {loading ? (
                <><Loader2 className="animate-spin mr-2" size={18} /> Analyzing...</>
              ) : (
                "Start Analysis"
              )}
            </button>
            <button className="btn-outline">View Reports</button>
          </div>
        </div>

        <div className="inference-ui-card surface-lowest razor-border ghost-shadow fade-in">
          <div className="card-header">
            <h3 className="text-sm font-bold uppercase tracking-wider">Live Inference Stage</h3>
          </div>
          
          <div className="upload-area surface-low razor-border">
            {image ? (
              <div className="preview-container">
                <img src={image} alt="Target" className="image-preview" />
                {!result && !loading && (
                    <button className="remove-btn" onClick={onReset}>×</button>
                )}
                {loading && (
                  <div className="loading-overlay glass">
                    <Loader2 className="animate-spin" size={32} color="var(--primary)" />
                    <span className="text-xs font-bold uppercase mt-2">Scanning Surface</span>
                  </div>
                )}
                {result && (
                  <div className="result-check">
                    <CheckCircle2 size={24} color="var(--secondary)" />
                  </div>
                )}
              </div>
            ) : (
              <label className="upload-label">
                <Upload size={32} className="mb-4 text-outline" />
                <span className="text-sm font-bold text-on-surface-variant">Drop image or click to upload</span>
                <span className="text-[10px] text-outline mt-2">Supports JPG, PNG (Max 10MB)</span>
                <input type="file" className="hidden" accept="image/*" onChange={(e) => onUpload(e.target.files[0])} />
              </label>
            )}
          </div>

          <div className="card-footer">
            {result ? (
              <div className="result-details fade-in">
                <div className="flex justify-between items-center mb-4">
                  <div className="flex items-center gap-2">
                    <span className="status-dot error"></span>
                    <span className="text-sm font-bold">{result.severity} {result.hazard_type}</span>
                  </div>
                  <span className="text-sm font-mono text-outline">{result.detection_id}</span>
                </div>
                <div className="stats-mini-grid flex justify-between">
                   <div className="stat-item">
                     <span className="label-sm text-outline">Confidence</span>
                     <span className="text-lg font-bold">{(result.confidence * 100).toFixed(1)}%</span>
                   </div>
                   <div className="stat-item text-right">
                     <span className="label-sm text-outline">Latitude</span>
                     <span className="text-lg font-bold">{result.metadata.lat}</span>
                   </div>
                </div>
              </div>
            ) : error ? (
              <div className="error-message flex items-center gap-2">
                <AlertCircle size={16} color="var(--error)" />
                <span className="text-xs text-error font-bold">{error}</span>
              </div>
            ) : (
              <p className="text-xs text-on-surface-variant italic">
                Upload image to begin precise infrastructure analysis.
              </p>
            )}
          </div>
        </div>
      </div>

      <style dangerouslySetInnerHTML={{ __html: `
        .hero-section {
          position: relative;
          min-height: 800px;
          padding: var(--spacing-24) 0;
          color: white;
        }
        .hero-background {
          position: absolute;
          inset: 0;
          z-index: 0;
        }
        .hero-image {
          width: 100%;
          height: 100%;
          object-fit: cover;
        }
        .hero-overlay {
          position: absolute;
          inset: 0;
          background: linear-gradient(to right, rgba(26, 28, 27, 0.95) 0%, rgba(26, 28, 27, 0.5) 50%, transparent 100%);
        }
        .hero-content-grid {
          display: grid;
          grid-template-columns: 1fr 400px;
          gap: var(--spacing-12);
          align-items: center;
        }
        .hero-title {
            color: #FFFFFF;
            font-size: 4.5rem;
            line-height: 0.95;
            letter-spacing: -0.05em;
        }
        .text-accent {
            color: var(--primary);
        }
        .hero-description {
            color: var(--surface-container-highest);
            font-size: 1.25rem;
            max-width: 480px;
            line-height: 1.6;
        }
        .label-pill {
            display: inline-block;
            background-color: var(--primary);
            color: white;
            padding: 0.35rem 1rem;
            border-radius: var(--radius-full);
        }
        
        /* Buttons */
        .btn-primary {
            background: linear-gradient(135deg, var(--primary) 0%, #1777c9 100%);
            color: white;
            padding: 1rem 2.5rem;
            border-radius: var(--radius-full);
            font-weight: 600;
            border: none;
            cursor: pointer;
            box-shadow: 0 10px 20px rgba(55, 138, 221, 0.2);
            transition: 0.2s;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .btn-primary:hover:not(:disabled) { transform: translateY(-2px); opacity: 0.9; }
        .btn-primary:disabled { opacity: 0.6; cursor: not-allowed; }
        
        .btn-outline {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            color: white;
            padding: 1rem 2.5rem;
            border-radius: var(--radius-full);
            font-weight: 600;
            border: 1px solid rgba(255, 255, 255, 0.2);
            cursor: pointer;
            transition: 0.2s;
        }
        .btn-outline:hover { background: rgba(255, 255, 255, 0.2); }

        /* Card */
        .inference-ui-card {
            border-radius: var(--radius-xl);
            padding: var(--spacing-6);
            color: var(--on-surface);
            transform: perspective(1000px) rotateY(-5deg);
        }
        .card-header { border-bottom: 1px solid var(--outline-variant); margin-bottom: var(--spacing-4); padding-bottom: var(--spacing-2); }
        
        .upload-area {
            height: 240px;
            border-radius: var(--radius-lg);
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            border: 1px dashed var(--outline);
        }
        .upload-label { cursor: pointer; text-align: center; padding: 2rem; width: 100%; height: 100%; display: flex; flex-direction: column; align-items: center; justify-content: center; }
        
        .preview-container { width: 100%; height: 100%; position: relative; }
        .image-preview { width: 100%; height: 100%; object-fit: cover; }
        .remove-btn { position: absolute; top: 10px; right: 10px; background: rgba(0,0,0,0.5); color: white; border: none; width: 24px; height: 24px; border-radius: 50%; cursor: pointer; }
        
        .loading-overlay { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; }
        .status-dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; }
        .status-dot.error { background-color: var(--error); }
        
        .result-check { position: absolute; bottom: 12px; right: 12px; background: white; border-radius: 50%; padding: 4px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        .card-footer { margin-top: var(--spacing-6); min-height: 60px; }
        
        .animate-spin { animation: spin 1s linear infinite; }
        @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
        
        @media (max-width: 1024px) {
            .hero-content-grid { grid-template-columns: 1fr; }
            .hero-title { font-size: 3rem; }
            .inference-ui-card { transform: none; max-width: 500px; margin: 0 auto; }
        }
      `}} />
    </section>
  );
};

export default HeroSection;
