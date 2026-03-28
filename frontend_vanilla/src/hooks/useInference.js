import { useState, useCallback } from 'react';

/**
 * useInference Hook
 * Cleanly separates the backend inference logic from the UI.
 * Handles state management for image processing and results.
 */
export const useInference = () => {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [image, setImage] = useState(null);

  const handleImageUpload = (file) => {
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (e) => {
      setImage(e.target.result);
    };
    reader.readAsDataURL(file);
    // Reset results on new upload
    setResult(null);
    setError(null);
  };

  const runAnalysis = useCallback(async () => {
    if (!image) {
      setError("Please upload an image first.");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      // Stub for backend API call (app.py)
      // Example: const response = await fetch('/predict', { method: 'POST', body: ... });
      
      // Simulating a network delay for the AI analysis
      await new Promise(resolve => setTimeout(resolve, 2400));
      
      // Mock result matching the "precision" and "editorial" requirements
      const mockResult = {
        hazard_type: "Pothole",
        confidence: 0.984,
        severity: "Critical",
        detection_id: "RS-8892-PT",
        metadata: {
          lat: "40.7128N",
          lng: "74.0060W",
          timestamp: new Date().toISOString()
        }
      };
      
      setResult(mockResult);
    } catch (err) {
      setError("Inference failed: " + err.message);
    } finally {
      setLoading(false);
    }
  }, [image]);

  const reset = () => {
    setImage(null);
    setResult(null);
    setError(null);
  };

  return {
    loading,
    image,
    result,
    error,
    handleImageUpload,
    runAnalysis,
    reset
  };
};
