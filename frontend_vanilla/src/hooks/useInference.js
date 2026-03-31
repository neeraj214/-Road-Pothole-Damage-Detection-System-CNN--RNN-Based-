import { useState, useEffect, useCallback, useRef } from 'react';
import { healthCheck, predict } from '../api';

// ─── localStorage helpers ────────────────────────────────────────────────────

const LS_KEY = 'roadsight_history';
const MAX_HISTORY = 100;

function loadHistory() {
  try {
    return JSON.parse(localStorage.getItem(LS_KEY) || '[]');
  } catch {
    return [];
  }
}

function saveHistory(entries) {
  localStorage.setItem(LS_KEY, JSON.stringify(entries));
}

function appendToHistory(entry) {
  const history = loadHistory();
  history.unshift(entry);               // newest first
  if (history.length > MAX_HISTORY) {
    history.length = MAX_HISTORY;       // drop oldest
  }
  saveHistory(history);
  return history;
}

// ─── Hook ────────────────────────────────────────────────────────────────────

/**
 * useInference — central state hook for RoadSight Precision Dashboard.
 *
 * Exposes:
 *  image          - base64 data-URL preview of selected file
 *  file           - the raw File object (kept for FormData upload)
 *  loading        - true while /predict request is in-flight
 *  result         - full JSON response from /predict, or null
 *  error          - error message string, or null
 *  apiOnline      - boolean: is the FastAPI backend reachable?
 *  history        - array of past predictions from localStorage
 *  handleImageUpload(event) - file input onChange handler
 *  handleFileDrop(file)     - raw File handler (from drag-and-drop)
 *  runAnalysis()            - triggers POST /predict
 */
export const useInference = () => {
  const [image, setImage]       = useState(null);   // data-URL for preview
  const [file, setFile]         = useState(null);   // raw File for upload
  const [loading, setLoading]   = useState(false);
  const [result, setResult]     = useState(null);
  const [error, setError]       = useState(null);
  const [apiOnline, setApiOnline] = useState(false);
  const [history, setHistory]   = useState(loadHistory);

  // ── Health-check polling (every 30 s) ─────────────────────────────────────
  const pollRef = useRef(null);

  const checkHealth = useCallback(async () => {
    const online = await healthCheck();
    setApiOnline(online);
  }, []);

  useEffect(() => {
    checkHealth();                                    // immediate on mount
    pollRef.current = setInterval(checkHealth, 30_000);
    return () => clearInterval(pollRef.current);
  }, [checkHealth]);

  // ── Internal: read a File into state ──────────────────────────────────────
  const loadFile = (f) => {
    if (!f) return;
    setFile(f);
    setResult(null);
    setError(null);
    const reader = new FileReader();
    reader.onloadend = () => setImage(reader.result);
    reader.readAsDataURL(f);
  };

  // ── Public: file-input onChange ────────────────────────────────────────────
  const handleImageUpload = (event) => {
    const f = event.target.files?.[0];
    if (f) loadFile(f);
  };

  // ── Public: drag-and-drop ──────────────────────────────────────────────────
  const handleFileDrop = (f) => {
    if (f) loadFile(f);
  };

  // ── Public: run analysis ───────────────────────────────────────────────────
  const runAnalysis = async () => {
    if (!file) return;
    setLoading(true);
    setResult(null);
    setError(null);

    try {
      const data = await predict(file);
      setResult(data);

      // Persist to localStorage
      const entry = {
        id: `${Date.now()}_${Math.random().toString(36).slice(2, 7)}`,
        filename: file.name,
        timestamp: new Date().toISOString(),
        imageDataUrl: image,   // data-URL captured when file was selected
        result: data,
      };
      const updated = appendToHistory(entry);
      setHistory(updated);
    } catch (err) {
      setError(err.message || 'Inference failed');
    } finally {
      setLoading(false);
    }
  };

  return {
    image,
    file,
    loading,
    result,
    error,
    apiOnline,
    history,
    handleImageUpload,
    handleFileDrop,
    runAnalysis,
  };
};
