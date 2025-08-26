import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import CreditAnalysis from './pages/CreditAnalysis';
import DataViewer from './pages/DataViewer';
import Reports from './pages/Reports';
import './styles/App.css';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/analysis" element={<CreditAnalysis />} />
            <Route path="/data" element={<DataViewer />} />
            <Route path="/reports" element={<Reports />} />
          </Routes>
        </main>
        <Toaster position="top-right" />
      </div>
    </Router>
  );
}

export default App;
