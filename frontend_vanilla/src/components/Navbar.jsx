import { Link, useLocation } from 'react-router-dom';
import { Search, Bell, Settings, Command } from 'lucide-react';

const Navbar = () => {
  const location = useLocation();

  return (
    <header className="navbar-container glass sticky-top">
      <div className="container nav-content flex items-center justify-between">
        <div className="flex items-center gap-8">
          <Link to="/" className="brand flex items-center gap-2">
            <Command size={24} color="var(--primary)" />
            <span className="brand-text">RoadSight Precision</span>
          </Link>
          <nav className="nav-links hidden md-flex">
            <Link to="/" className={location.pathname === '/' ? 'active' : ''}>Home</Link>
            <Link to="/dashboard" className={location.pathname === '/dashboard' ? 'active' : ''}>Dashboard</Link>
            <a href="#">Analysis</a>
            <a href="#">Reports</a>
          </nav>
        </div>
        
        <div className="flex items-center gap-3">
          <div className="search-box relative hidden sm-block">
            <Search className="search-icon" size={16} />
            <input 
              type="text" 
              placeholder="Search systems..." 
              className="search-input surface-lowest razor-border" 
            />
          </div>
          <div className="nav-actions flex items-center gap-1">
            <button className="icon-btn"><Bell size={18} /></button>
            <button className="icon-btn"><Settings size={18} /></button>
          </div>
          <div className="user-avatar-container ml-2">
            <div className="user-avatar razor-border">
              <img 
                src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=facearea&facepad=2&w=256&h=256&q=80" 
                alt="User" 
              />
            </div>
          </div>
        </div>
      </div>

      <style dangerouslySetInnerHTML={{ __html: `
        .navbar-container {
          width: 100%;
          height: 64px;
          z-index: 1000;
          position: sticky;
          top: 0;
          border-bottom: 1px solid var(--outline-variant);
        }
        .nav-content {
          height: 100%;
          display: flex;
          align-items: center;
          justify-content: space-between;
        }
        .brand-text {
          font-weight: 800;
          font-size: 1.125rem;
          color: var(--primary);
          letter-spacing: -0.04em;
        }
        .nav-links {
          display: flex;
          gap: var(--spacing-6);
        }
        .nav-links a {
          font-weight: 500;
          font-size: 0.875rem;
          color: var(--on-surface-variant);
          padding: 0.25rem 0.75rem;
          border-radius: var(--radius-md);
        }
        .nav-links a:hover {
          background-color: var(--surface-container-low);
          color: var(--on-surface);
        }
        .nav-links a.active {
          color: var(--primary);
          font-weight: 600;
        }
        .search-box .search-icon {
          position: absolute;
          left: 12px;
          top: 50%;
          transform: translateY(-50%);
          color: var(--outline);
        }
        .search-input {
          padding: 0.375rem 1rem 0.375rem 2.25rem;
          border-radius: var(--radius-full);
          font-size: 0.875rem;
          width: 240px;
          outline: none;
          transition: 0.2s;
        }
        .search-input:focus {
          border-color: var(--primary);
          box-shadow: 0 0 0 2px rgba(55, 138, 221, 0.1);
        }
        .icon-btn {
          background: none;
          border: none;
          padding: 0.5rem;
          border-radius: var(--radius-full);
          color: var(--on-surface-variant);
          cursor: pointer;
          transition: 0.15s;
        }
        .icon-btn:hover {
          background-color: var(--surface-container-low);
          color: var(--on-surface);
        }
        .user-avatar {
          width: 32px;
          height: 32px;
          border-radius: var(--radius-full);
          overflow: hidden;
        }
        .user-avatar img {
          width: 100%;
          height: 100%;
          object-fit: cover;
        }
        .flex { display: flex; }
        .items-center { align-items: center; }
        .justify-between { justify-content: space-between; }
        .gap-1 { gap: var(--spacing-1); }
        .gap-2 { gap: var(--spacing-2); }
        .gap-3 { gap: var(--spacing-3); }
        .gap-8 { gap: var(--spacing-8); }
        .ml-2 { margin-left: var(--spacing-2); }
        .relative { position: relative; }
        @media (max-width: 768px) { .hidden { display: none; } }
      `}} />
    </header>
  );
};

export default Navbar;
