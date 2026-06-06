import { Link } from 'react-router-dom'
import { 
  BarChart3, Shield, Cpu, Cloud, AlertTriangle, Database, 
  ArrowRight, Wheat, Droplets, Thermometer 
} from 'lucide-react'

export default function HomePage() {
  return (
    <>
      {/* ── Hero Section ─────────────────────────────────── */}
      <section className="hero-section" id="main-content">
        <div className="container">
          <div className="hero-content">
            <div className="hero-left">
              <h1>
                <span className="hindi-text">किसान उपज रक्षक</span>
                Kisan Yield Guard
              </h1>
              <p>
                AI-powered district-level crop yield prediction system for Indian agriculture. 
                Leveraging XGBoost machine learning, MLflow experiment tracking, and Evidently AI 
                drift detection to safeguard farmers across <strong>16 states</strong> and{' '}
                <strong>30 districts</strong>.
              </p>
              <div className="hero-buttons">
                <Link to="/predict" className="btn btn-primary btn-lg">
                  <BarChart3 size={18} />
                  Predict Yield
                </Link>
                <Link to="/pipeline" className="btn btn-secondary btn-lg">
                  View Pipeline
                  <ArrowRight size={18} />
                </Link>
              </div>
              <div className="hero-stats">
                <div className="hero-stat-card">
                  <div className="stat-number">16</div>
                  <div className="stat-label">States Covered</div>
                </div>
                <div className="hero-stat-card">
                  <div className="stat-number">30</div>
                  <div className="stat-label">Districts</div>
                </div>
                <div className="hero-stat-card">
                  <div className="stat-number">3</div>
                  <div className="stat-label">Crops Tracked</div>
                </div>
              </div>
            </div>
            <div className="hero-right">
              <div className="hero-illustration">
                <span className="emoji-icon">🌾</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ── Key Features ─────────────────────────────────── */}
      <section className="section">
        <div className="container">
          <div className="section-header">
            <div className="hindi-label">मुख्य विशेषताएँ</div>
            <h2>Key Features of the System</h2>
            <p>
              A complete MLOps lifecycle designed for production-grade crop yield prediction
            </p>
          </div>

          <div className="features-grid">
            <div className="feature-card">
              <div className="card-icon saffron">
                <Cpu size={28} />
              </div>
              <h3>XGBoost ML Model</h3>
              <p>
                Gradient-boosted decision tree model trained on 5,000+ records with 
                real Indian agricultural parameters — rainfall, temperature, soil type, 
                irrigation, and CACP MSP data from 2010–2023.
              </p>
            </div>

            <div className="feature-card">
              <div className="card-icon navy">
                <Database size={28} />
              </div>
              <h3>MLflow Experiment Tracking</h3>
              <p>
                Every training run is logged with metrics (RMSE, MAE, R²), hyperparameters, 
                and feature importance plots. Models are versioned and promoted through 
                Staging → Production stages.
              </p>
            </div>

            <div className="feature-card">
              <div className="card-icon green">
                <AlertTriangle size={28} />
              </div>
              <h3>Evidently AI Drift Detection</h3>
              <p>
                Automated detection of data drift using Kolmogorov-Smirnov and Chi-Square tests. 
                Simulates El Niño and drought scenarios with reduced rainfall (−25%) and 
                elevated temperatures (+2°C).
              </p>
            </div>

            <div className="feature-card">
              <div className="card-icon saffron">
                <Shield size={28} />
              </div>
              <h3>Quality Gates (R² &gt; 0.75)</h3>
              <p>
                No model reaches production without passing automated evaluation gates. 
                Only models exceeding the R² threshold of 0.75 are promoted to the 
                MLflow Production registry.
              </p>
            </div>

            <div className="feature-card">
              <div className="card-icon navy">
                <BarChart3 size={28} />
              </div>
              <h3>FastAPI Serving Endpoint</h3>
              <p>
                Production REST API built with FastAPI + Pydantic validation. 
                Returns predicted yield (kg/ha), yield category (Low/Medium/High), 
                and model version metadata with every response.
              </p>
            </div>

            <div className="feature-card">
              <div className="card-icon green">
                <Cloud size={28} />
              </div>
              <h3>CI/CD Auto-Retraining</h3>
              <p>
                GitHub Actions workflow runs drift checks quarterly. If significant drift 
                is detected (&gt;15% features), the pipeline automatically retrains, 
                evaluates, and deploys the updated model.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* ── Crops Covered ────────────────────────────────── */}
      <section className="section" style={{ background: 'white' }}>
        <div className="container">
          <div className="section-header">
            <div className="hindi-label">समर्थित फसलें</div>
            <h2>Crops Covered Under This Scheme</h2>
            <p>Prediction support for India's three major crops with real MSP data</p>
          </div>

          <div className="features-grid">
            <div className="feature-card" style={{ borderTopColor: '#2E7D32' }}>
              <div className="card-icon green">
                <Wheat size={28} />
              </div>
              <h3>🌾 Rice (धान)</h3>
              <p>
                <strong>Season:</strong> Kharif (Monsoon)<br />
                <strong>Yield Range:</strong> 1,500 – 4,500 kg/ha<br />
                <strong>Optimal Temp:</strong> 27°C<br />
                <strong>MSP 2023:</strong> ₹2,183/quintal<br />
                <strong>Best Soil:</strong> Alluvial
              </p>
            </div>

            <div className="feature-card" style={{ borderTopColor: '#E65100' }}>
              <div className="card-icon saffron">
                <Wheat size={28} />
              </div>
              <h3>🌾 Wheat (गेहूं)</h3>
              <p>
                <strong>Season:</strong> Rabi (Winter)<br />
                <strong>Yield Range:</strong> 1,800 – 5,000 kg/ha<br />
                <strong>Optimal Temp:</strong> 20°C<br />
                <strong>MSP 2023:</strong> ₹2,125/quintal<br />
                <strong>Best Soil:</strong> Alluvial
              </p>
            </div>

            <div className="feature-card" style={{ borderTopColor: '#1565C0' }}>
              <div className="card-icon navy">
                <Droplets size={28} />
              </div>
              <h3>🍬 Sugarcane (गन्ना)</h3>
              <p>
                <strong>Season:</strong> Kharif / Zaid<br />
                <strong>Yield Range:</strong> 40,000 – 90,000 kg/ha<br />
                <strong>Optimal Temp:</strong> 30°C<br />
                <strong>MSP 2023:</strong> ₹3,150/quintal<br />
                <strong>Best Soil:</strong> Black
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* ── States Coverage ──────────────────────────────── */}
      <section className="section">
        <div className="container">
          <div className="section-header">
            <div className="hindi-label">राज्य कवरेज</div>
            <h2>States & Districts Covered</h2>
            <p>Spanning 16 major agricultural states across India</p>
          </div>

          <div style={{ 
            display: 'grid', 
            gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', 
            gap: '12px' 
          }}>
            {[
              { state: 'Punjab', districts: 'Ludhiana, Amritsar, Patiala' },
              { state: 'Haryana', districts: 'Karnal, Hisar' },
              { state: 'Uttar Pradesh', districts: 'Lucknow, Meerut, Gorakhpur' },
              { state: 'Bihar', districts: 'Patna, Muzaffarpur' },
              { state: 'West Bengal', districts: 'Bardhaman, Hooghly' },
              { state: 'Maharashtra', districts: 'Nashik, Pune, Kolhapur' },
              { state: 'Andhra Pradesh', districts: 'Guntur, Krishna' },
              { state: 'Tamil Nadu', districts: 'Coimbatore, Thanjavur' },
              { state: 'Karnataka', districts: 'Belgaum, Mysore' },
              { state: 'Madhya Pradesh', districts: 'Indore, Jabalpur' },
              { state: 'Rajasthan', districts: 'Jaipur, Jodhpur' },
              { state: 'Odisha', districts: 'Cuttack' },
              { state: 'Chhattisgarh', districts: 'Raipur' },
              { state: 'Telangana', districts: 'Warangal' },
              { state: 'Gujarat', districts: 'Ahmedabad' },
              { state: 'Assam', districts: 'Nagaon' },
            ].map(s => (
              <div key={s.state} style={{
                background: 'white',
                border: '1px solid var(--gov-border)',
                borderLeft: '4px solid var(--navy)',
                borderRadius: 'var(--radius-sm)',
                padding: '14px 16px',
                transition: 'all 0.25s',
                cursor: 'default',
              }}
              onMouseEnter={e => {
                e.currentTarget.style.borderLeftColor = 'var(--saffron)'
                e.currentTarget.style.transform = 'translateX(4px)'
              }}
              onMouseLeave={e => {
                e.currentTarget.style.borderLeftColor = 'var(--navy)'
                e.currentTarget.style.transform = 'translateX(0)'
              }}
              >
                <div style={{ fontWeight: 700, color: 'var(--navy)', fontSize: '0.9rem', marginBottom: '4px' }}>
                  {s.state}
                </div>
                <div style={{ fontSize: '0.78rem', color: 'var(--gov-text-muted)' }}>
                  {s.districts}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── CTA ──────────────────────────────────────────── */}
      <section className="section" style={{ 
        background: 'linear-gradient(135deg, var(--navy-dark), var(--navy))',
        padding: '48px 0'
      }}>
        <div className="container" style={{ textAlign: 'center' }}>
          <h2 style={{ color: 'white', fontSize: '1.6rem', marginBottom: '12px' }}>
            Ready to Predict Crop Yield?
          </h2>
          <p style={{ color: 'rgba(255,255,255,0.7)', marginBottom: '24px', fontSize: '0.95rem' }}>
            Enter your district details, weather data, and soil parameters to get an instant AI-powered prediction
          </p>
          <div style={{ display: 'flex', gap: '14px', justifyContent: 'center', flexWrap: 'wrap' }}>
            <Link to="/predict" className="btn btn-primary btn-lg">
              <BarChart3 size={18} />
              Start Prediction
            </Link>
            <Link to="/drift" className="btn btn-secondary btn-lg">
              <AlertTriangle size={18} />
              Check Drift Status
            </Link>
          </div>
        </div>
      </section>
    </>
  )
}
