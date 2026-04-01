/**
 * RoadSight Precision — API Client
 * Base URL: FastAPI backend running on http://localhost:8000
 */

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

/**
 * Check backend health.
 * Returns true if the API is online and model is loaded, false otherwise.
 */
export async function healthCheck() {
  try {
    const res = await fetch(`${BASE_URL}/health`, { method: 'GET' });
    if (!res.ok) return false;
    const data = await res.json();
    return data.model_loaded === true;
  } catch {
    return false;
  }
}

/**
 * Run road surface prediction on an image file.
 * @param {File} file - The image file to analyse.
 * @returns {Promise<Object>} Full response JSON from /predict.
 * @throws {Error} If the request fails or returns a non-ok status.
 */
export async function predict(file) {
  const formData = new FormData();
  formData.append('file', file);

  const res = await fetch(`${BASE_URL}/predict`, {
    method: 'POST',
    body: formData,
    // Do NOT set Content-Type header — browser sets it with correct boundary for multipart
  });

  if (!res.ok) {
    let detail = `HTTP ${res.status}`;
    try {
      const err = await res.json();
      detail = err.detail || detail;
    } catch { /* ignore parse errors */ }
    throw new Error(detail);
  }

  return res.json();
}
