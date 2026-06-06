import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { useState, useEffect } from 'react'
import AccessibilityBar from './components/AccessibilityBar'
import TricolorStripe from './components/TricolorStripe'
import Header from './components/Header'
import NavBar from './components/NavBar'
import Ticker from './components/Ticker'
import Footer from './components/Footer'
import ScrollToTop from './components/ScrollToTop'
import HomePage from './pages/HomePage'
import PredictPage from './pages/PredictPage'
import DriftPage from './pages/DriftPage'
import PipelinePage from './pages/PipelinePage'
import AboutPage from './pages/AboutPage'
import './App.css'

function App() {
  return (
    <Router>
      <div id="app-wrapper">
        <AccessibilityBar />
        <TricolorStripe />
        <Header />
        <NavBar />
        <Ticker />
        <main>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/predict" element={<PredictPage />} />
            <Route path="/drift" element={<DriftPage />} />
            <Route path="/pipeline" element={<PipelinePage />} />
            <Route path="/about" element={<AboutPage />} />
          </Routes>
        </main>
        <Footer />
        <ScrollToTop />
      </div>
    </Router>
  )
}

export default App
