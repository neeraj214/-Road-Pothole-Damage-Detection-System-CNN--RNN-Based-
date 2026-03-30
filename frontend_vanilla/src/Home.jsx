import { useInference } from './hooks/useInference';
import { Link } from 'react-router-dom';

/**
 * RoadSight Precision | AI Infrastructure Monitoring
 * Recreated Production Landing Page (Stitch Design)
 */
const Home = () => {
  const { image, loading, result, handleImageUpload, runAnalysis } = useInference();

  return (
    <div className="bg-background text-on-surface font-Inter selection:bg-primary-fixed selection:text-on-primary-fixed antialiased transition-colors duration-300">
      {/* TopAppBar */}
      <header className="sticky top-0 w-full z-40 bg-surface/90 backdrop-blur-md border-b border-black/5 shadow-[0px_12px_32px_rgba(25,28,29,0.04)]">
        <div className="flex items-center justify-between px-6 h-16 w-full max-w-7xl mx-auto">
          <div className="flex items-center gap-8">
            <span className="text-lg font-bold tracking-tighter text-primary">RoadSight Precision</span>
            <nav className="hidden md:flex items-center gap-6 antialiased tracking-tight text-sm font-medium text-on-surface-variant">
              <a className="text-primary font-semibold" href="#">Home</a>
              <Link className="hover:bg-surface-container-low transition-colors duration-200 px-3 py-1 rounded-lg" to="/dashboard">Dashboard</Link>
              <a className="hover:bg-surface-container-low transition-colors duration-200 px-3 py-1 rounded-lg" href="#">Analysis</a>
              <a className="hover:bg-surface-container-low transition-colors duration-200 px-3 py-1 rounded-lg" href="#">Reports</a>
            </nav>
          </div>
          <div className="flex items-center gap-3">
            <div className="relative hidden sm:block">
              <span className="absolute left-3 top-1/2 -translate-y-1/2 material-symbols-outlined text-outline text-sm opacity-50">search</span>
              <input 
                className="bg-surface-container-lowest border-none rounded-full pl-10 pr-4 py-1.5 text-sm w-64 focus:ring-2 focus:ring-primary/20 transition-all outline-none" 
                placeholder="Search systems..." 
                type="text"
              />
            </div>
            <div className="flex items-center gap-1">
              <button className="p-2 rounded-full hover:bg-surface-container-low text-on-surface-variant transition-colors"><span className="material-symbols-outlined">api</span></button>
              <button className="p-2 rounded-full hover:bg-surface-container-low text-on-surface-variant transition-colors"><span className="material-symbols-outlined">notifications</span></button>
              <button className="p-2 rounded-full hover:bg-surface-container-low text-on-surface-variant transition-colors"><span className="material-symbols-outlined">settings</span></button>
            </div>
            <img 
              alt="User Profile" 
              className="w-8 h-8 rounded-full object-cover ml-2 border border-black/5" 
              src="https://lh3.googleusercontent.com/aida-public/AB6AXuD613Q7HChbhKHkOIPM8Ij76vA0s-_1G4SxgEcbgzeDo7xIXLFs2wa9auRjYc-dpdTG2nXbgIrmBXkVh-28lwYCmoq1Z2sN7M-8_hDnJF5mDUAnujc0vLkJWdBsDK44ywjWtB65SK3udEP8ljOF3SUViB73cMyJ9IqCERdmJPQoSAnBTgPsw9sTh4F1XSsUPt5oFzi3tTQtxqT3unjpyleHWggm5ElqVpw7k8nxSS7vYfzJT1XwqIoRDvuiOR3-_ImwNPje1embnnyL"
            />
          </div>
        </div>
      </header>

      <main>
        {/* Hero Section */}
        <section className="relative h-hero flex items-center overflow-hidden">
          <div className="absolute inset-0 z-0">
            <img 
              alt="Twilight Highway Bridge" 
              className="w-full h-full object-cover" 
              src="https://lh3.googleusercontent.com/aida-public/AB6AXuAB_JCLdk6wIOa7rBD_loX1aOb6o9l5lpxAyoQhvcPtvscZRG55UwxIiW4gX-SdY6o0p5eQ4W7bvW05x_OPkfeQ1N_WMQJsFsCDSUt75TUlKWMFdLhREBuaBvBeNBxPDQTegIDwdEvuKJ-fspH-O9W19mfdHJFamWSumi7uwD6E-ssZ7oB-qB48mJHdN90BCb8HexbrdjFy468YH2K8p3LYE0OJ7V9_uRXWYJX36B6QRshTJh4NYels68gFM0V2t3RvMXExQbq0fsHI"
            />
            <div className="absolute inset-0 bg-gradient-to-r from-on-surface/90 via-on-surface/40 to-transparent"></div>
          </div>
          <div className="container mx-auto px-6 relative z-10">
            <div className="max-w-3xl fade-in">
              <span className="inline-block px-4 py-1.5 bg-primary-container text-on-primary-container rounded-full text-[0.6875rem] font-bold tracking-[0.05em] uppercase mb-6">
                Infrastructure Intelligence
              </span>
              <h1 className="text-5xl md:text-7xl font-bold text-white tracking-tighter leading-[0.95] mb-8">
                The Future of <br/><span className="text-primary-fixed">Digital Surveying.</span>
              </h1>
              <p className="text-lg md:text-xl text-surface-variant max-w-xl mb-10 leading-relaxed text-slate-300">
                Harness the power of high-precision AI to monitor, detect, and prioritize road maintenance with surgical accuracy.
              </p>
              
              <div className="flex flex-wrap gap-4">
                <label className="bg-gradient-to-br from-primary to-primary-container text-white px-10 py-4 rounded-full font-semibold shadow-lg hover:opacity-90 transition-all active:scale-[0.98] cursor-pointer inline-flex items-center justify-center">
                  {loading ? 'Processing...' : 'Start Analysis'}
                  <input type="file" className="hidden" onChange={handleImageUpload} disabled={loading} accept="image/*" />
                </label>
                <button className="px-10 py-4 rounded-full font-semibold border border-white/20 text-white backdrop-blur-md hover:bg-white/10 transition-all">
                  View Reports
                </button>
              </div>

              {/* Inference Result Overlay */}
              {image && (
                <div className="mt-12 p-6 bg-white/10 backdrop-blur-xl border border-white/10 rounded-2xl max-w-xl fade-in group">
                  <div className="flex items-center gap-4 mb-4">
                    <div className="w-2 h-2 bg-primary rounded-full animate-pulse"></div>
                    <span className="text-white text-[0.6875rem] font-bold uppercase tracking-widest opacity-80">System Ready</span>
                  </div>
                  <img src={image} alt="Inference Target" className="w-full h-40 object-cover rounded-xl mb-4 grayscale group-hover:grayscale-0 transition-all duration-700" />
                  <button 
                    onClick={runAnalysis} 
                    className="w-full py-3 bg-white text-primary font-bold rounded-xl hover:bg-primary-fixed transition-colors text-sm uppercase tracking-wider"
                    disabled={loading}
                  >
                    {loading ? 'Executing Neural Logic...' : 'Run Diagnostics'}
                  </button>
                  {result && (
                    <div className="mt-4 p-4 bg-primary/20 rounded-lg text-white font-bold text-center border border-white/10 shadow-lg animate-bounce">
                      Detection: {result.class} ({Math.round(result.confidence * 100)}%)
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        </section>

        {/* Value Proposition Bento */}
        <section className="py-24 bg-surface-container-low">
          <div className="container mx-auto px-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {[
                { title: "AI-Powered Monitoring", icon: "memory", desc: "Real-time infrastructure oversight using advanced neural networks.", color: "bg-primary/10 text-primary hover:bg-primary" },
                { title: "Precision Detection", icon: "gps_fixed", desc: "Sub-millimeter accuracy in identifying potholes and surface cracks.", color: "bg-secondary-container/20 text-on-secondary-container hover:bg-secondary-container" },
                { title: "Repair Priority", icon: "priority_high", desc: "Automated scoring system factors in hazard severity and traffic.", color: "bg-tertiary-container/10 text-tertiary hover:bg-tertiary-container" }
              ].map((card, idx) => (
                <div key={idx} className="bg-surface-container-lowest p-10 rounded-lg flex flex-col gap-4 shadow-sm group hover:translate-y-[-4px] transition-transform duration-300">
                  <div className={`w-12 h-12 rounded-xl flex items-center justify-center transition-colors ${card.color} group-hover:text-white`}>
                    <span className="material-symbols-outlined">{card.icon}</span>
                  </div>
                  <h3 className="text-xl font-bold tracking-tight text-on-surface">{card.title}</h3>
                  <p className="text-on-surface-variant text-sm leading-relaxed">{card.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Statistics Row */}
        <section className="py-20 bg-primary overflow-hidden">
          <div className="container mx-auto px-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-12 text-center">
              {[
                { value: "12.8k", label: "Roads Scanned" },
                { value: "98.4%", label: "Detection Accuracy" },
                { value: "2.4s", label: "Processing Time" }
              ].map((stat, idx) => (
                <div key={idx} className="flex flex-col gap-2">
                  <span className="text-primary-fixed text-6xl font-black tracking-tighter">{stat.value}</span>
                  <span className="text-on-primary/80 uppercase tracking-widest text-[0.6875rem] font-bold">{stat.label}</span>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Technical Detail Section */}
        <section className="py-32 bg-surface overflow-hidden">
          <div className="container mx-auto px-6">
            <div className="flex flex-col lg:flex-row items-center gap-20">
              <div className="flex-1 space-y-12">
                <div>
                  <span className="text-primary font-bold tracking-widest text-[0.6875rem] uppercase">Technical Specs</span>
                  <h2 className="text-4xl font-bold tracking-tighter text-on-surface mt-4 mb-6 leading-tight text-slate-800">Sophisticated Detection <br/>Simplified Execution</h2>
                </div>
                <div className="space-y-8">
                  {[
                    { title: "Computer Vision", desc: "Proprietary camera fusion models trained on 50M+ anomalies.", icon: "visibility" },
                    { title: "Automated Priority Scoring", desc: "Dynamic algorithms calculate Risk-to-Public metrics.", icon: "assessment" },
                    { title: "Cloud Reporting", desc: "Geo-tagged PDF and JSON reports for stakeholders.", icon: "cloud_sync" }
                  ].map((spec, idx) => (
                    <div key={idx} className="flex gap-6">
                      <div className="shrink-0 w-14 h-14 bg-surface-container-highest rounded-full flex items-center justify-center">
                        <span className="material-symbols-outlined text-primary">{spec.icon}</span>
                      </div>
                      <div>
                        <h4 className="text-lg font-bold text-on-surface mb-1">{spec.title}</h4>
                        <p className="text-on-surface-variant text-sm max-w-sm">{spec.desc}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
              
              <div className="flex-1 relative">
                <div className="absolute -top-10 -left-10 w-64 h-64 bg-primary/5 rounded-full blur-3xl"></div>
                <div className="relative bg-surface-container-highest p-4 rounded-xl shadow-2xl overflow-hidden group">
                  <img 
                    alt="System Tablet Interface" 
                    className="rounded-lg w-full aspect-[4/3] object-cover transition-transform duration-700 group-hover:scale-105" 
                    src="https://lh3.googleusercontent.com/aida-public/AB6AXuBQFJNXU0Ts3YwZ_qT654th9riVTZIuN-Caa0hPNVTjOKRZepMrR0Jw6JAGwXdoxJS1hHonIFZgdCBShv40or8JurGYnLEsf234sE8NwXKJLgN62IZV5gFSCEQVoxH5WCffPXAzMF2HQ516pvMI6g2q7ZhzfQzuYW6N0z-dFZYitLR3Js3YmTgWfCkCJ6ybilCjE2qzXR2HF3AMgL87PR5SUhAfW_KtDyG7sUge0lScyx5JWEKm1E08Ty4yGNDkW5aCDBzeOTWZGN7c"
                  />
                  <div className="absolute top-10 right-10 bg-tertiary-container text-on-tertiary-container px-4 py-2 rounded-full flex items-center gap-2 shadow-lg glass-effect">
                    <span className="w-2 h-2 bg-white rounded-full animate-pulse"></span>
                    <span className="text-[0.6875rem] font-bold uppercase tracking-wider">Critical Hazard Detected</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-24">
          <div className="container mx-auto px-6">
            <div className="bg-slate-900 rounded-2xl p-12 md:p-20 text-center relative overflow-hidden group shadow-2xl">
              <div className="absolute inset-0 opacity-10 transition-opacity duration-700 group-hover:opacity-20 grayscale">
                <img 
                  alt="Texture Background" 
                  className="w-full h-full object-cover scale-110 group-hover:scale-100 transition-transform duration-1000" 
                  src="https://lh3.googleusercontent.com/aida-public/AB6AXuB67U8nk7Q4nRnfQiqi0T-U7rHSzSaFuB6UABVN7xBZLmeDCwjUw4ebsxU7b8j-LvBcHsK3ylwtlxk1m-fvLtcnC8HqUqnLU8BJ-JwD-clHa5uAvCKy7QABBAAKLclTSl3ED1_Z2KqzmCHrKBX5Xg162cshGnb_B02TXcgBY2NMFUA6PY1tBoObGX5y4NQ1nnGc02uj_4Tijk4ofB1jN2aMHq_X2uiNzx3mBS5I2Evs82sVk8_a2tKQOfJ8ykEsP1edzGnu61aHvQNq"
                />
              </div>
              <div className="relative z-10 max-w-2xl mx-auto">
                <h2 className="text-4xl md:text-5xl font-bold text-white tracking-tighter mb-8 leading-tight">Ready to modernize your infrastructure?</h2>
                <div className="flex flex-wrap justify-center gap-4">
                  <button className="bg-primary text-white px-10 py-4 rounded-full font-semibold hover:bg-primary-container transition-all shadow-lg active:scale-95">Get Started Free</button>
                  <button className="bg-white/10 text-white px-10 py-4 rounded-full font-semibold border border-white/20 backdrop-blur-sm hover:bg-white/20 transition-all active:scale-95">Talk to Sales</button>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="bg-surface-container-low py-16 border-t border-black/5">
        <div className="container mx-auto px-6">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-12 mb-16">
            <div className="col-span-1 md:col-span-1">
              <span className="text-lg font-bold tracking-tighter text-primary">RoadSight Precision</span>
              <p className="text-on-surface-variant text-sm mt-4 leading-relaxed font-Inter">Defining the next generation of civil engineering through artificial intelligence.</p>
            </div>
            {['Product', 'Company', 'Legal'].map((title, idx) => (
              <div key={idx}>
                <h5 className="font-bold text-on-surface mb-6 uppercase text-[0.6875rem] tracking-widest">{title}</h5>
                <ul className="space-y-4 text-sm text-on-surface-variant">
                  {['Link 1', 'Link 2', 'Link 3'].map((item, i) => (
                    <li key={i}><a className="hover:text-primary transition-colors" href="#">{item}</a></li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
          <div className="pt-8 border-t border-outline-variant/30 flex flex-col md:flex-row justify-between items-center gap-4">
            <p className="text-[0.6875rem] text-on-surface-variant font-medium tracking-wide">© 2024 ROADSIGHT PRECISION. ALL RIGHTS RESERVED.</p>
            <div className="flex gap-6">
              <span className="material-symbols-outlined text-on-surface-variant hover:text-primary cursor-pointer transition-colors">share</span>
              <span className="material-symbols-outlined text-on-surface-variant hover:text-primary cursor-pointer transition-colors">language</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Home;
