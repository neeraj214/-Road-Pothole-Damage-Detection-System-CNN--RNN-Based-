import React from 'react';
import { LayoutDashboard, Home, BarChart2, History, FileText, HelpCircle, LogOut } from 'lucide-react';
import { Link, useLocation } from 'react-router-dom';

const Sidebar = () => {
  const location = useLocation();

  const menuItems = [
    { icon: <LayoutDashboard size={20} />, label: 'Dashboard', path: '/dashboard' },
    { icon: <Home size={20} />, label: 'Home', path: '/' },
    { icon: <BarChart2 size={20} />, label: 'Analysis', path: '#' },
    { icon: <History size={20} />, label: 'History', path: '#' },
    { icon: <FileText size={20} />, label: 'Reports', path: '#' },
  ];

  return (
    <aside className="sidebar surface-low flex flex-col pt-6">
      <div className="px-6 mb-8 sidebar-brand">
        <h1 className="brand-label">Modern Precision</h1>
        <p className="version-label">Digital Surveyor v2.1</p>
      </div>
      
      <nav className="flex flex-col gap-1 px-3">
        {menuItems.map((item, i) => (
          <Link 
            key={i} 
            to={item.path} 
            className={`nav-item flex items-center gap-3 ${location.pathname === item.path ? 'active' : ''}`}
          >
            {item.icon}
            <span className="text-sm font-medium">{item.label}</span>
          </Link>
        ))}
      </nav>

      <div className="mt-auto px-3 pb-6">
        <div className="border-top pt-4 mb-4">
          <a href="#" className="nav-item flex items-center gap-3 opacity-70">
            <HelpCircle size={18} />
            <span className="text-sm font-medium">Support</span>
          </a>
        </div>
        
        <div className="user-profile-mini flex items-center gap-3 p-3 surface-lowest razor-border">
          <div className="avatar-initials flex items-center justify-center">JD</div>
          <div className="user-info overflow-hidden">
            <p className="text-xs font-bold truncate">John Doe</p>
            <p className="text-[10px] text-zinc-500 truncate">Admin Access</p>
          </div>
        </div>
      </div>

      <style dangerouslySetInnerHTML={{ __html: `
        .sidebar {
          width: 256px;
          height: 100vh;
          position: fixed;
          left: 0;
          top: 0;
          z-index: 50;
          border-right: 1px solid var(--outline-variant);
        }
        .brand-label {
          font-size: 0.6875rem;
          font-weight: 900;
          text-transform: uppercase;
          letter-spacing: 0.05em;
          color: var(--on-surface);
        }
        .version-label {
          font-size: 10px;
          color: var(--outline);
          font-weight: 500;
        }
        .nav-item {
          padding: 0.75rem 1rem;
          border-radius: var(--radius-md);
          color: var(--on-surface-variant);
          transition: all 0.2s;
        }
        .nav-item:hover {
          background-color: var(--surface-container);
          transform: translateX(4px);
        }
        .nav-item.active {
          background: linear-gradient(135deg, var(--primary) 0%, #1777c9 100%);
          color: white;
          box-shadow: var(--shadow-ghost);
        }
        .avatar-initials {
          width: 32px;
          height: 32px;
          border-radius: var(--radius-sm);
          background-color: var(--primary-container);
          color: var(--primary);
          font-size: 10px;
          font-weight: 700;
          flex-shrink: 0;
        }
        .user-profile-mini {
          border-radius: var(--radius-md);
        }
        .border-top { border-top: 1px solid var(--outline-variant); }
      `}} />
    </aside>
  );
};

export default Sidebar;
