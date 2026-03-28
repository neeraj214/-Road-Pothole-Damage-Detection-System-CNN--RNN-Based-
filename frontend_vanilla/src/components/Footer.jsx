import React from 'react';
import { Share2, Globe } from 'lucide-react';

const Footer = () => {
  return (
    <footer className="footer-container surface-low py-16">
      <div className="container">
        <div className="grid grid-footer gap-12 mb-16">
          <div className="brand-col">
            <span className="brand-text text-primary">RoadSight Precision</span>
            <p className="brand-slogan text-sm mt-4 leading-relaxed">
              Defining the next generation of civil engineering through artificial intelligence and precision surveying.
            </p>
          </div>
          
          <div className="links-col">
            <h5 className="label-sm mb-6">Product</h5>
            <ul className="footer-links">
              <li><a href="#">Features</a></li>
              <li><a href="#">Integration</a></li>
              <li><a href="#">Case Studies</a></li>
              <li><a href="#">Pricing</a></li>
            </ul>
          </div>
          
          <div className="links-col">
            <h5 className="label-sm mb-6">Company</h5>
            <ul className="footer-links">
              <li><a href="#">About Us</a></li>
              <li><a href="#">Engineering</a></li>
              <li><a href="#">Careers</a></li>
              <li><a href="#">Contact</a></li>
            </ul>
          </div>
          
          <div className="links-col">
            <h5 className="label-sm mb-6">Legal</h5>
            <ul className="footer-links">
              <li><a href="#">Privacy Policy</a></li>
              <li><a href="#">Terms of Service</a></li>
              <li><a href="#">Cookie Policy</a></li>
            </ul>
          </div>
        </div>

        <div className="footer-bottom pt-8 border-top flex justify-between items-center gap-4">
          <p className="copyright label-sm">© 2024 ROADSIGHT PRECISION. ALL RIGHTS RESERVED.</p>
          <div className="flex gap-6">
            <a href="#" className="social-link"><Share2 size={18} /></a>
            <a href="#" className="social-link"><Globe size={18} /></a>
          </div>
        </div>
      </div>

      <style dangerouslySetInnerHTML={{ __html: `
        .footer-container { border-top: 1px solid var(--outline-variant); }
        .grid-footer { display: grid; grid-template-columns: 2fr repeat(3, 1fr); gap: var(--spacing-12); }
        .brand-text { font-weight: 800; font-size: 1.125rem; }
        .brand-slogan { color: var(--on-surface-variant); max-width: 240px; }
        .footer-links { list-style: none; padding: 0; }
        .footer-links li { margin-bottom: 0.75rem; }
        .footer-links a { font-size: 0.875rem; color: var(--on-surface-variant); }
        .footer-links a:hover { color: var(--primary); }
        
        .footer-bottom { border-top: 1px solid rgba(113, 119, 131, 0.1); margin-top: 4rem; padding-top: 2rem; }
        .copyright { color: var(--on-surface-variant); opacity: 0.8; }
        .social-link { color: var(--on-surface-variant); transition: 0.2s; }
        .social-link:hover { color: var(--primary); }
        
        @media (max-width: 768px) {
            .grid-footer { grid-template-columns: 1fr 1fr; }
            .brand-col { grid-column: span 2; }
        }
      `}} />
    </footer>
  );
};

export default Footer;
