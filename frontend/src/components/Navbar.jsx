import { Link } from 'react-router-dom';
import { HiGlobeAmericas } from 'react-icons/hi2';
import { motion } from 'framer-motion';

function Navbar() {
  return (
    <nav className="sticky top-0 z-50 bg-white/70 backdrop-blur-md border-b border-slate-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex-shrink-0">
            <Link to="/" className="flex items-center space-x-2">
              <HiGlobeAmericas className="h-8 w-8 text-primary" />
              <span className="font-bold text-xl text-slate-900 tracking-tight">RoadAI</span>
            </Link>
          </div>
          <div className="hidden md:block">
            <div className="ml-10 flex items-baseline space-x-4">
              <Link to="/" className="text-slate-600 hover:text-primary px-3 py-2 rounded-md text-sm font-medium transition-colors">Home</Link>
              <Link to="/detect" className="text-slate-600 hover:text-primary px-3 py-2 rounded-md text-sm font-medium transition-colors">Detect</Link>
              <a href="https://github.com/neeraj214" className="text-slate-600 hover:text-primary px-3 py-2 rounded-md text-sm font-medium transition-colors">GitHub</a>
            </div>
          </div>
          <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
            <Link to="/detect" className="bg-primary text-white px-4 py-2 rounded-full text-sm font-semibold shadow-sm hover:bg-blue-600 transition-colors">
              Start Detection
            </Link>
          </motion.div>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
