import React from 'react';
import { Eye, BarChart3, Cloud } from 'lucide-react';

const FeatureDetail = () => {
  const features = [
    {
      icon: <Eye size={24} />,
      title: "Computer Vision",
      description: "Proprietary LiDAR and camera fusion models trained on over 50 million road anomalies globally."
    },
    {
      icon: <BarChart3 size={24} />,
      title: "Automated Priority Scoring",
      description: "Dynamic algorithms calculate the Cost-to-Repair vs. Risk-to-Public metrics in real-time."
    },
    {
      icon: <Cloud size={24} />,
      title: "Cloud Reporting",
      description: "Seamlessly push data to municipal stakeholders with interactive, geo-tagged PDF and JSON reports."
    }
  ];

  return (
    <section className="feature-detail-section py-32 overflow-hidden surface-lowest">
      <div className="container">
        <div className="grid grid-2 items-center gap-24">
          <div className="feature-text-block space-y-12">
            <div>
              <span className="label-sm text-primary mb-4 block">Technical Specs</span>
              <h2 className="display-md mb-6 leading-tight">Sophisticated Detection <br/>Simplified Execution</h2>
            </div>
            
            <div className="feature-list space-y-8">
              {features.map((f, i) => (
                <div key={i} className="feature-item flex gap-6">
                  <div className="feature-icon-circle surface-container-highest flex center">
                    {f.icon}
                  </div>
                  <div>
                    <h4 className="text-lg font-bold mb-2">{f.title}</h4>
                    <p className="text-on-surface-variant text-sm max-w-md">{f.description}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="feature-visual-block relative">
             <div className="visual-background-blobs">
                <div className="blob blob-1"></div>
                <div className="blob blob-2"></div>
             </div>
             
             <div className="main-visual-container surface-container-highest razor-border ghost-shadow">
                <img 
                  src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=2560&auto=format&fit=crop" 
                  alt="System Interface" 
                  className="visual-image"
                />
                
                {/* Floating Hazard Chip as specified in DESIGN.md */}
                <div className="hazard-chip-floating glass ghost-shadow flex items-center gap-2">
                   <div className="pulse-dot"></div>
                   <span className="label-sm tracking-wider">Critical Hazard Detected</span>
                </div>
             </div>
          </div>
        </div>
      </div>

      <style dangerouslySetInnerHTML={{ __html: `
        .feature-detail-section { position: relative; }
        .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: var(--spacing-24); align-items: center; }
        .feature-icon-circle {
            width: 56px; height: 56px; border-radius: var(--radius-full);
            color: var(--primary); flex-shrink: 0;
            display: flex; align-items: center; justify-content: center;
        }
        .main-visual-container {
            border-radius: var(--radius-xl); padding: var(--spacing-4);
            position: relative; overflow: hidden;
            z-index: 5;
        }
        .visual-image { width: 100%; aspect-ratio: 4/3; border-radius: var(--radius-lg); object-fit: cover; }
        
        .hazard-chip-floating {
            position: absolute; top: var(--spacing-8); right: var(--spacing-8);
            background: rgba(226, 75, 74, 0.9); border: 1px solid rgba(255,255,255,0.2);
            color: white; padding: 0.5rem 1rem; border-radius: var(--radius-full);
        }
        
        .pulse-dot { width: 8px; height: 8px; background: white; border-radius: 50%; animation: pulse 2s infinite; }
        @keyframes pulse { 0% { opacity: 1; transform: scale(1); } 50% { opacity: 0.5; transform: scale(1.2); } 100% { opacity: 1; transform: scale(1); } }
        
        .blob { position: absolute; width: 300px; height: 300px; filter: blur(100px); opacity: 0.15; border-radius: 50%; z-index: 1; }
        .blob-1 { top: -50px; left: -50px; background-color: var(--primary); }
        .blob-2 { bottom: -50px; right: -50px; background-color: var(--secondary); }
        
        .center { display: flex; align-items: center; justify-content: center; }
        .space-y-8 > * + * { margin-top: 2rem; }
        .space-y-12 > * + * { margin-top: 3rem; }
        @media (max-width: 1024px) { .grid-2 { grid-template-columns: 1fr; gap: var(--spacing-12); } }
      `}} />
    </section>
  );
};

export default FeatureDetail;
