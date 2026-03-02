import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Detect from './pages/Detect';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-background text-slate-900 selection:bg-primary selection:text-white">
        <Navbar />
        <main>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/detect" element={<Detect />} />
          </Routes>
        </main>
        <footer className="py-8 text-center text-slate-500 border-t border-slate-200">
          <p>© 2026 Road Pothole Detection System • Developed by <a href="https://github.com/neeraj214" className="text-primary hover:underline">Neeraj Negi</a></p>
        </footer>
      </div>
    </Router>
  );
}

export default App;
