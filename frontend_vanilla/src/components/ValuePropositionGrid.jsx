import React from 'react';
import { Cpu, Target, Zap } from 'lucide-react';

const ValuePropositionGrid = () => {
  const cards = [
    {
      icon: <Cpu size={24} />,
      title: "AI-Powered Monitoring",
      description: "Real-time infrastructure oversight using advanced neural networks to identify subtle decay patterns before they fail.",
      color: "var(--primary)"
    },
    {
      icon: <Target size={24} />,
      title: "Precision Detection",
      description: "Sub-millimeter accuracy in identifying potholes, surface cracks, and structural anomalies across thousands of miles.",
      color: "var(--secondary)"
    },
    {
      icon: <Zap size={24} />,
      title: "Network Optimization",
      description: "Automated scoring system that factors in traffic volume and hazard severity to optimize your maintenance budget.",
      color: "var(--tertiary)"
    }
  ];

  return (
    <section className="value-prop-section surface-low py-24">
      <div className="container">
        <div className="grid grid-3 gap-8">
          {cards.map((card, i) => (
            <div key={i} className="prop-card surface-lowest razor-border ghost-shadow fade-in">
              <div className="icon-wrapper" style={{ color: card.color, backgroundColor: `${card.color}15` }}>
                {card.icon}
              </div>
              <h3 className="card-title mt-4 mb-2">{card.title}</h3>
              <p className="card-text text-sm">{card.description}</p>
            </div>
          ))}
        </div>
      </div>

      <style dangerouslySetInnerHTML={{ __html: `
        .grid-3 {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: var(--spacing-8);
        }
        .prop-card {
            padding: var(--spacing-12);
            border-radius: var(--radius-lg);
            transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .prop-card:hover {
            transform: translateY(-8px);
        }
        .icon-wrapper {
            width: 48px;
            height: 48px;
            border-radius: var(--radius-md);
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .card-title {
            font-size: 1.25rem;
            letter-spacing: -0.02em;
        }
        .card-text {
            color: var(--on-surface-variant);
            line-height: 1.6;
        }
        @media (max-width: 900px) {
            .grid-3 { grid-template-columns: 1fr; }
        }
      `}} />
    </section>
  );
};

export default ValuePropositionGrid;
