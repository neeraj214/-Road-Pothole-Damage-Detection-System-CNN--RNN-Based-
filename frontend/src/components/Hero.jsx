import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { HiArrowRight } from 'react-icons/hi2';

function Hero() {
  return (
    <div className="relative overflow-hidden bg-background py-24 sm:py-32">
      <div className="mx-auto max-w-7xl px-6 lg:px-8">
        <div className="mx-auto max-w-2xl text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <h1 className="text-4xl font-bold tracking-tight text-slate-900 sm:text-6xl">
              Advanced <span className="text-primary">Road Damage</span> Detection System
            </h1>
            <p className="mt-6 text-lg leading-8 text-slate-600">
              Utilizing state-of-the-art CNN architecture to automatically identify potholes, cracks, and road hazards with high precision.
            </p>
            <div className="mt-10 flex items-center justify-center gap-x-6">
              <motion.div whileHover={{ x: 5 }}>
                <Link
                  to="/detect"
                  className="rounded-full bg-primary px-8 py-4 text-sm font-semibold text-white shadow-lg hover:bg-blue-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary flex items-center gap-2"
                >
                  Analyze Road <HiArrowRight className="w-4 h-4" />
                </Link>
              </motion.div>
              <a href="https://github.com/neeraj214" className="text-sm font-semibold leading-6 text-slate-900 hover:text-primary transition-colors">
                View on GitHub <span aria-hidden="true">→</span>
              </a>
            </div>
          </motion.div>
        </div>
      </div>
      
      {/* Decorative background elements */}
      <div className="absolute top-0 left-1/2 -z-10 -translate-x-1/2 blur-3xl" aria-hidden="true">
        <div className="aspect-[1155/678] w-[72.1875rem] bg-gradient-to-tr from-[#3b82f6] to-[#93c5fd] opacity-20"></div>
      </div>
    </div>
  );
}

export default Hero;
