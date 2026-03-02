import { useState, useCallback } from 'react';
import { motion } from 'framer-motion';
import { HiCloudArrowUp, HiXMark } from 'react-icons/hi2';

function UploadBox({ onUpload }) {
  const [isDragging, setIsDragging] = useState(false);
  const [preview, setPreview] = useState(null);

  const handleFile = (file) => {
    if (file && file.type.startsWith('image/')) {
      const reader = new FileReader();
      reader.onload = () => setPreview(reader.result);
      reader.readAsDataURL(file);
      onUpload(file);
    }
  };

  const onDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const onDragLeave = () => {
    setIsDragging(false);
  };

  const onDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files[0];
    handleFile(file);
  };

  const clearFile = (e) => {
    e.stopPropagation();
    setPreview(null);
    onUpload(null);
  };

  return (
    <motion.div
      whileHover={{ scale: 1.01 }}
      className={`relative group cursor-pointer border-2 border-dashed rounded-3xl p-12 transition-all duration-200 ${
        isDragging ? 'border-primary bg-blue-50' : 'border-slate-200 hover:border-primary/50 bg-white'
      }`}
      onDragOver={onDragOver}
      onDragLeave={onDragLeave}
      onDrop={onDrop}
      onClick={() => document.getElementById('file-upload').click()}
    >
      <input
        id="file-upload"
        type="file"
        className="hidden"
        accept="image/*"
        onChange={(e) => handleFile(e.target.files[0])}
      />

      {preview ? (
        <div className="relative aspect-video rounded-2xl overflow-hidden shadow-sm">
          <img src={preview} alt="Preview" className="w-full h-full object-cover" />
          <button
            onClick={clearFile}
            className="absolute top-4 right-4 p-2 bg-white/80 backdrop-blur rounded-full text-slate-900 hover:bg-white transition-colors"
          >
            <HiXMark className="w-5 h-5" />
          </button>
        </div>
      ) : (
        <div className="flex flex-col items-center justify-center text-center">
          <div className="p-4 bg-blue-50 rounded-full mb-4 group-hover:bg-blue-100 transition-colors">
            <HiCloudArrowUp className="w-8 h-8 text-primary" />
          </div>
          <h3 className="text-lg font-semibold text-slate-900">Upload road image</h3>
          <p className="mt-2 text-sm text-slate-500">Drag and drop or click to browse</p>
          <p className="mt-1 text-xs text-slate-400">Supports JPG, PNG, WEBP</p>
        </div>
      )}
    </motion.div>
  );
}

export default UploadBox;
