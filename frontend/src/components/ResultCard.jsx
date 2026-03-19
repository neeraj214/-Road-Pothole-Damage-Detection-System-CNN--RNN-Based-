import { motion } from 'framer-motion';
import { HiCheckCircle, HiExclamationTriangle, HiShieldExclamation, HiOutlineDocumentText } from 'react-icons/hi2';
import { useEffect, useRef } from 'react';

function ResultCard({ result, file }) {
  const { class: prediction, confidence, rps_score, mask } = result;
  const confidencePercent = (confidence * 100).toFixed(1);
  const canvasRef = useRef(null);

  const getTheme = () => {
    switch (prediction.toLowerCase()) {
      case 'normal':
      case 'good road':
      case 'healthy road':
        return {
          color: 'text-success',
          bg: 'bg-green-50',
          icon: <HiCheckCircle className="w-8 h-8 text-success" />,
          label: 'Healthy Road'
        };
      case 'crack':
      case 'surface crack':
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

  useEffect(() => {
    if (mask && file && canvasRef.current) {
      const canvas = canvasRef.current;
      const ctx = canvas.getContext('2d');
      const img = new Image();
      const maskImg = new Image();

      img.onload = () => {
        // Match canvas size to image aspect ratio but keep it responsive
        const maxWidth = canvas.parentElement.clientWidth;
        const scale = maxWidth / img.width;
        canvas.width = img.width * scale;
        canvas.height = img.height * scale;

        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

        maskImg.onload = () => {
          // Create an offscreen canvas for the mask
          const maskCanvas = document.createElement('canvas');
          maskCanvas.width = canvas.width;
          maskCanvas.height = canvas.height;
          const maskCtx = maskCanvas.getContext('2d');
          
          maskCtx.drawImage(maskImg, 0, 0, canvas.width, canvas.height);
          
          // Map mask values (0, 1, 2, 3) to different colors
          const severityColors = {
            0: [0, 0, 0, 0],       // Background: Transparent
            1: [253, 224, 71, 140], // Hairline: Yellow (70% opacity)
            2: [251, 146, 60, 160], // Alligator: Orange (80% opacity)
            3: [239, 68, 68, 180]   // Deep Pothole: Red (90% opacity)
          };

          for (let i = 0; i < data.length; i += 4) {
            const classIdx = data[i]; // The value from the single-channel PNG (0, 1, 2, 3)
            const color = severityColors[classIdx] || [0, 0, 0, 0];
            
            data[i] = color[0];     // R
            data[i + 1] = color[1]; // G
            data[i + 2] = color[2]; // B
            data[i + 3] = color[3]; // A
          }
          
          maskCtx.putImageData(imageData, 0, 0);
          ctx.drawImage(maskCanvas, 0, 0);
        };
        maskImg.src = `data:image/png;base64,${mask}`;
      };
      img.src = URL.createObjectURL(file);
    }
  }, [mask, file, prediction]);

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className="bg-white rounded-3xl p-8 shadow-glass border border-white overflow-hidden relative"
    >
      <div className={`absolute top-0 left-0 w-2 h-full ${theme.color.replace('text-', 'bg-')}`} />
      
      <div className="flex flex-col lg:flex-row gap-8">
        {/* Left: Visualization */}
        <div className="w-full lg:w-1/2">
          <div className="rounded-2xl overflow-hidden border border-slate-100 bg-slate-50">
            <canvas ref={canvasRef} className="w-full h-auto block" />
          </div>
          <div className="mt-4 flex flex-wrap justify-center gap-4">
            <div className="flex items-center gap-1.5 text-[10px] font-medium text-slate-500">
              <span className="w-3 h-3 rounded-sm bg-yellow-300"></span> Hairline
            </div>
            <div className="flex items-center gap-1.5 text-[10px] font-medium text-slate-500">
              <span className="w-3 h-3 rounded-sm bg-orange-400"></span> Alligator
            </div>
            <div className="flex items-center gap-1.5 text-[10px] font-medium text-slate-500">
              <span className="w-3 h-3 rounded-sm bg-red-500"></span> Deep Pothole
            </div>
          </div>
          <p className="mt-2 text-xs text-center text-slate-400 italic">Severity Segmentation Overlay</p>
        </div>

        {/* Right: Results Data */}
        <div className="w-full lg:w-1/2 flex flex-col justify-between">
          <div>
            <div className="flex items-start justify-between mb-8">
              <div className="flex items-center gap-4">
                <div className={`p-3 rounded-2xl ${theme.bg}`}>
                  {theme.icon}
                </div>
                <div>
                  <h3 className="text-sm font-medium text-slate-500 uppercase tracking-wider">Status</h3>
                  <p className={`text-2xl font-bold ${theme.color}`}>{theme.label}</p>
                </div>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-6 mb-8">
              <div className="p-4 bg-slate-50 rounded-2xl">
                <h3 className="text-xs font-medium text-slate-500 uppercase tracking-wider mb-1">Confidence</h3>
                <p className="text-xl font-bold text-slate-900">{confidencePercent}%</p>
              </div>
              <div className="p-4 bg-slate-50 rounded-2xl">
                <h3 className="text-xs font-medium text-slate-500 uppercase tracking-wider mb-1">RPS Score</h3>
                <p className={`text-xl font-bold ${rps_score > 5 ? 'text-danger' : 'text-slate-900'}`}>
                  {rps_score}%
                </p>
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
          </div>
          
          <div className="mt-8 lg:mt-0 p-5 bg-blue-50/50 border border-blue-100/50 rounded-2xl">
            <div className="flex items-start gap-3">
              <HiOutlineDocumentText className="w-5 h-5 text-blue-500 mt-0.5" />
              <div className="text-sm text-slate-600 leading-relaxed">
                <span className="font-semibold text-blue-700">Analysis Summary:</span>
                <p className="mt-1">
                  Our system identifies <span className="font-semibold">{theme.label}</span> with <span className="font-semibold">{confidencePercent}%</span> certainty. 
                  The Road Pothole Severity (RPS) score is <span className="font-semibold">{rps_score}%</span>.
                </p>
                <p className="mt-2 text-xs">
                  {rps_score > 10 ? 
                    "⚠️ Urgent repair recommended due to high damage density." : 
                    rps_score > 5 ? 
                    "🔔 Moderate damage detected. Schedule maintenance soon." : 
                    "✅ Low severity. Regular monitoring suggested."}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
}

export default ResultCard;
