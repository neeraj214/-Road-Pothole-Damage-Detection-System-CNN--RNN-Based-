import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import UploadBox from '../components/UploadBox';
import ResultCard from '../components/ResultCard';
import Loader from '../components/Loader';
import { predictPothole } from '../api';
import { HiSparkles } from 'react-icons/hi2';

function Detect() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleAnalyze = async () => {
    if (!file) return;

    setLoading(true);
    setError(null);
    setResult(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const data = await predictPothole(formData);
      setResult(data);
    } catch (err) {
      setError("Failed to analyze image. Please ensure the backend server is running.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-6 py-12 lg:py-24">
      <div className="text-center mb-12">
        <h2 className="text-3xl font-bold text-slate-900 flex items-center justify-center gap-2">
          Analyze Road Surface <HiSparkles className="text-primary" />
        </h2>
        <p className="mt-4 text-slate-600">Upload a photo of the road to detect potential damages using AI.</p>
      </div>

      <div className="space-y-8">
        <UploadBox onUpload={setFile} />

        <div className="flex justify-center">
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={handleAnalyze}
            disabled={!file || loading}
            className={`px-12 py-4 rounded-full font-bold text-white shadow-lg transition-all duration-200 ${
              !file || loading 
                ? 'bg-slate-300 cursor-not-allowed shadow-none' 
                : 'bg-primary hover:bg-blue-600 active:bg-blue-700'
            }`}
          >
            {loading ? 'Analyzing...' : 'Analyze Road'}
          </motion.button>
        </div>

        <AnimatePresence mode="wait">
          {loading && (
            <motion.div
              key="loader"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              <Loader />
            </motion.div>
          )}

          {result && (
            <motion.div
              key="result"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
            >
              <ResultCard result={result} file={file} />
            </motion.div>
          )}

          {error && (
            <motion.div
              key="error"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="p-4 bg-red-50 border border-red-100 text-red-600 rounded-2xl text-center text-sm font-medium"
            >
              {error}
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}

export default Detect;
