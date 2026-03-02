import { motion } from 'framer-motion';

function Loader() {
  return (
    <div className="flex flex-col items-center justify-center p-12 text-center">
      <div className="relative w-16 h-16">
        <motion.div
          animate={{
            scale: [1, 1.2, 1],
            rotate: [0, 180, 360],
            borderRadius: ["20%", "50%", "20%"]
          }}
          transition={{
            duration: 2,
            repeat: Infinity,
            ease: "easeInOut"
          }}
          className="w-full h-full border-4 border-primary/30 border-t-primary rounded-xl"
        />
      </div>
      <h3 className="mt-6 text-lg font-semibold text-slate-900">Analyzing Road Surface</h3>
      <p className="mt-2 text-sm text-slate-500 animate-pulse">Running CNN detection models...</p>
    </div>
  );
}

export default Loader;
