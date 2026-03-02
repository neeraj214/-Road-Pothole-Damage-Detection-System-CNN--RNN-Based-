import { motion } from 'framer-motion';
import { HiCheckCircle, HiExclamationTriangle, HiShieldExclamation } from 'react-icons/hi2';

function ResultCard({ result }) {
  const { class: prediction, confidence } = result;
  const confidencePercent = (confidence * 100).toFixed(1);

  const getTheme = () => {
    switch (prediction.toLowerCase()) {
      case 'normal':
      case 'good road':
        return {
          color: 'text-success',
          bg: 'bg-green-50',
          icon: <HiCheckCircle className="w-8 h-8 text-success" />,
          label: 'Healthy Road'
        };
      case 'crack':
        return {
          color: 'text-warning',
          bg: 'bg-yellow-50',
          icon: <HiExclamationTriangle className="w-8 h-8 text-warning" />,
          label: 'Surface Crack'
        };
      case 'pothole':
        return {
          color: 'text-danger',
          bg: 'bg-red-50',
          icon: <HiShieldExclamation className="w-8 h-8 text-danger" />,
          label: 'Pothole Detected'
        };
      default:
        return {
          color: 'text-primary',
          bg: 'bg-blue-50',
          icon: <HiCheckCircle className="w-8 h-8 text-primary" />,
          label: prediction
        };
    }
  };

  const theme = getTheme();

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className="bg-white rounded-3xl p-8 shadow-glass border border-white overflow-hidden relative"
    >
      <div className={`absolute top-0 left-0 w-2 h-full ${theme.color.replace('text-', 'bg-')}`} />
      
      <div className="flex items-start justify-between mb-8">
        <div className="flex items-center gap-4">
          <div className={`p-3 rounded-2xl ${theme.bg}`}>
            {theme.icon}
          </div>
          <div>
            <h3 className="text-sm font-medium text-slate-500 uppercase tracking-wider">Classification</h3>
            <p className={`text-2xl font-bold ${theme.color}`}>{theme.label}</p>
          </div>
        </div>
        <div className="text-right">
          <h3 className="text-sm font-medium text-slate-500 uppercase tracking-wider">Confidence</h3>
          <p className="text-2xl font-bold text-slate-900">{confidencePercent}%</p>
        </div>
      </div>

      <div className="relative h-2 w-full bg-slate-100 rounded-full overflow-hidden">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${confidencePercent}%` }}
          transition={{ duration: 1, ease: "easeOut" }}
          className={`absolute top-0 left-0 h-full rounded-full ${theme.color.replace('text-', 'bg-')}`}
        />
      </div>
      
      <p className="mt-6 text-sm text-slate-500 leading-relaxed">
        Our system analyzed the uploaded image and identified the road condition as <span className="font-semibold">{theme.label}</span> with <span className="font-semibold">{confidencePercent}%</span> certainty.
      </p>
    </motion.div>
  );
}

export default ResultCard;
