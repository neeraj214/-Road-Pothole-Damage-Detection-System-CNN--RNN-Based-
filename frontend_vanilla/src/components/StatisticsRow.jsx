import React from 'react';

const StatisticsRow = () => {
  const stats = [
    { value: "12.8k", label: "Roads Scanned" },
    { value: "98.4%", label: "Detection Accuracy" },
    { value: "2.4s", label: "Processing Time" }
  ];

  return (
    <section className="stats-section bg-primary py-20">
      <div className="container">
        <div className="grid grid-3-stats text-center items-center">
          {stats.map((stat, i) => (
            <div key={i} className="stat-unit fade-in" style={{ animationDelay: `${i * 0.1}s` }}>
              <div className="stat-value">{stat.value}</div>
              <div className="stat-label label-sm">{stat.label}</div>
            </div>
          ))}
        </div>
      </div>

      <style dangerouslySetInnerHTML={{ __html: `
        .stats-section {
          background-color: var(--primary);
          color: white;
          overflow: hidden;
        }
        .grid-3-stats {
          display: grid;
          grid-template-columns: repeat(3, 1fr);
          gap: var(--spacing-12);
        }
        .stat-value {
          font-size: 4rem;
          font-weight: 900;
          letter-spacing: -0.06em;
          line-height: 1;
          color: white;
          margin-bottom: var(--spacing-2);
        }
        .stat-label {
          color: rgba(255, 255, 255, 0.7);
          tracking: 0.15em;
        }
        @media (max-width: 768px) {
            .grid-3-stats { grid-template-columns: 1fr; gap: var(--spacing-8); }
            .stat-value { font-size: 3rem; }
        }
      `}} />
    </section>
  );
};

export default StatisticsRow;
