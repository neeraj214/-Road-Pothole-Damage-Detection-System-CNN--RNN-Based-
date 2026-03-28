import React from 'react';
import Navbar from '../components/Navbar';
import HeroSection from '../components/HeroSection';
import ValuePropositionGrid from '../components/ValuePropositionGrid';
import StatisticsRow from '../components/StatisticsRow';
import FeatureDetail from '../components/FeatureDetail';
import Footer from '../components/Footer';
import { useInference } from '../hooks/useInference';

const Home = () => {
  const inference = useInference();

  return (
    <div className="home-page">
      <Navbar />
      
      <main>
        <HeroSection 
          image={inference.image}
          loading={inference.loading}
          result={inference.result}
          error={inference.error}
          onUpload={inference.handleImageUpload}
          onAnalyze={inference.runAnalysis}
          onReset={inference.reset}
        />
        
        <ValuePropositionGrid />
        
        <StatisticsRow />
        
        <FeatureDetail />
        
        <section className="cta-section py-24">
          <div className="container">
            <div className="cta-card surface-high p-20 text-center relative overflow-hidden razor-border ghost-shadow">
              <div className="cta-background-texture opacity-10"></div>
              <div className="relative z-10 max-w-2xl mx-auto">
                <h2 className="display-md mb-8">Ready to modernize your infrastructure?</h2>
                <div className="flex justify-center gap-4">
                  <button className="btn-primary">Get Started Free</button>
                  <button className="btn-outline text-on-surface">Talk to Sales</button>
                </div>
              </div>
            </div>
          </div>
          <style dangerouslySetInnerHTML={{ __html: `
            .cta-card {
                border-radius: var(--radius-xl);
                background-color: var(--on-surface);
                color: white;
            }
            .cta-card .display-md { color: white; }
            .cta-background-texture {
                position: absolute;
                inset: 0;
                background-image: url('https://images.unsplash.com/photo-1562654501-a0ccc0fc3fb1?q=80&w=2000&auto=format&fit=crop');
                background-size: cover;
                background-position: center;
                pointer-events: none;
            }
          `}} />
        </section>
      </main>

      <Footer />
    </div>
  );
};

export default Home;
