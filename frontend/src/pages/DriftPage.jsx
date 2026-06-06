import { useState } from 'react'
import { Link } from 'react-router-dom'
import { 
  AlertTriangle, RefreshCw, Shield, Activity, 
  TrendingDown, CheckCircle, XCircle, Loader2 
} from 'lucide-react'

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export default function DriftPage() {
  const [drift, setDrift] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const checkDrift = async () => {
    setLoading(true)
    setError(null)

    try {
      const res = await fetch(`${API_BASE}/drift-status`)
      if (!res.ok) {
        const err = await res.json()
        throw new Error(err.detail || `HTTP ${res.status}`)
      }
      const data = await res.json()
      setDrift(data)
    } catch (err) {
      setError(err.message || 'Could not connect to the API. Ensure FastAPI server is running on port 8000.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      {/* Page Banner */}
      <div className="page-banner">
        <div className="container">
          <h1>⚠️ Data Drift Monitoring</h1>
          <div className="breadcrumb">
            <Link to="/">Home</Link> &nbsp;›&nbsp; Drift Detection
          </div>
        </div>
      </div>

      <div className="drift-page">
        <div className="container">

          {/* Introduction */}
          <div style={{
            background: 'white',
            borderRadius: 'var(--radius-md)',
            padding: '28px',
            marginBottom: '28px',
            boxShadow: 'var(--shadow-sm)',
            border: '1px solid var(--gov-border)',
          }}>
            <h2 style={{ color: 'var(--navy)', fontSize: '1.2rem', marginBottom: '12px' }}>
              About Data Drift Detection
            </h2>
            <p style={{ color: 'var(--gov-text-muted)', fontSize: '0.9rem', lineHeight: 1.8, marginBottom: '16px' }}>
              In Indian agriculture, shifting <strong>monsoon patterns</strong>, <strong>El Niño events</strong>, 
              and <strong>drought conditions</strong> can drastically alter crop yields, rendering ML models obsolete. 
              Kisan Yield Guard uses <strong>Evidently AI</strong> to continuously monitor the incoming data distribution 
              against the reference baseline using <strong>Kolmogorov-Smirnov</strong> (numerical) and{' '}
              <strong>Chi-Square</strong> (categorical) statistical tests.
            </p>
            <p style={{ color: 'var(--gov-text-muted)', fontSize: '0.9rem', lineHeight: 1.8, marginBottom: '20px' }}>
              <strong>Drift Threshold:</strong> If more than <strong>15%</strong> of features show statistically 
              significant drift, an alert is raised and the CI/CD pipeline triggers automatic retraining.
            </p>
            <button className="btn btn-navy btn-lg" onClick={checkDrift} disabled={loading}>
              {loading ? (
                <>
                  <Loader2 size={18} style={{ animation: 'spin 0.8s linear infinite' }} />
                  Running Drift Check...
                </>
              ) : (
                <>
                  <RefreshCw size={18} />
                  Run Drift Detection Now
                </>
              )}
            </button>
          </div>

          {/* Error */}
          {error && (
            <div className="error-toast">
              ⚠️ {error}
            </div>
          )}

          {/* Loading */}
          {loading && (
            <div className="loading-spinner" style={{ padding: '60px' }}>
              <div className="spinner" />
            </div>
          )}

          {/* Results */}
          {drift && !loading && (
            <>
              {/* Alert Banner */}
              <div className={`drift-alert ${drift.drift_detected ? 'danger' : 'success'}`}>
                <span className="alert-icon">
                  {drift.drift_detected ? <XCircle size={28} /> : <CheckCircle size={28} />}
                </span>
                <div>
                  <strong>{drift.drift_detected ? '🚨 DRIFT DETECTED' : '✅ NO DRIFT DETECTED'}</strong>
                  <div style={{ fontSize: '0.85rem', marginTop: '4px', opacity: 0.85 }}>
                    {drift.details}
                  </div>
                </div>
              </div>

              {/* Stats Grid */}
              <div className="drift-grid">
                <div className="drift-stat-card">
                  <div className="drift-stat-icon" style={{
                    background: drift.drift_detected ? 'rgba(197,48,48,0.1)' : 'rgba(19,136,8,0.1)',
                    color: drift.drift_detected ? 'var(--gov-red)' : 'var(--green)',
                  }}>
                    <Shield size={24} />
                  </div>
                  <div className="drift-stat-info">
                    <h3>Drift Status</h3>
                    <div className="stat-value" style={{
                      color: drift.drift_detected ? 'var(--gov-red)' : 'var(--green)',
                    }}>
                      {drift.drift_detected ? 'DETECTED' : 'STABLE'}
                    </div>
                    <div className="stat-subtitle">
                      {drift.drift_detected ? 'Retraining recommended' : 'Model is performing well'}
                    </div>
                  </div>
                </div>

                <div className="drift-stat-card">
                  <div className="drift-stat-icon" style={{
                    background: 'rgba(0,51,102,0.1)',
                    color: 'var(--navy)',
                  }}>
                    <Activity size={24} />
                  </div>
                  <div className="drift-stat-info">
                    <h3>Drifted Features</h3>
                    <div className="stat-value">
                      {drift.drifted_features} / {drift.total_features}
                    </div>
                    <div className="stat-subtitle">
                      Features showing significant distribution shift
                    </div>
                  </div>
                </div>

                <div className="drift-stat-card">
                  <div className="drift-stat-icon" style={{
                    background: 'rgba(255,153,51,0.1)',
                    color: 'var(--saffron-dark)',
                  }}>
                    <TrendingDown size={24} />
                  </div>
                  <div className="drift-stat-info">
                    <h3>Drift Share</h3>
                    <div className="stat-value">
                      {drift.drift_share_pct}%
                    </div>
                    <div className="stat-subtitle">
                      Percentage of features drifted (threshold: 15%)
                    </div>
                  </div>
                </div>

                <div className="drift-stat-card">
                  <div className="drift-stat-icon" style={{
                    background: 'rgba(19,136,8,0.1)',
                    color: 'var(--green)',
                  }}>
                    <AlertTriangle size={24} />
                  </div>
                  <div className="drift-stat-info">
                    <h3>Action Required</h3>
                    <div className="stat-value" style={{ fontSize: '1.1rem' }}>
                      {drift.drift_detected ? 'Retrain Model' : 'None'}
                    </div>
                    <div className="stat-subtitle">
                      {drift.drift_detected
                        ? 'Run CI/CD pipeline to retrain XGBoost model'
                        : 'System is healthy, next check scheduled quarterly'
                      }
                    </div>
                  </div>
                </div>
              </div>

              {/* Drift Simulation Info */}
              <div style={{
                background: 'white',
                borderRadius: 'var(--radius-md)',
                padding: '24px',
                boxShadow: 'var(--shadow-sm)',
                border: '1px solid var(--gov-border)',
                borderLeft: '4px solid var(--saffron)',
              }}>
                <h3 style={{ color: 'var(--navy)', fontSize: '1rem', marginBottom: '12px' }}>
                  🌧️ Drought Simulation Details
                </h3>
                <p style={{ color: 'var(--gov-text-muted)', fontSize: '0.88rem', lineHeight: 1.8 }}>
                  The drift batch (<code>drift_batch.csv</code>) simulates a severe drought / El Niño event:
                </p>
                <ul style={{
                  margin: '12px 0',
                  paddingLeft: '20px',
                  color: 'var(--gov-text-muted)',
                  fontSize: '0.88rem',
                  lineHeight: 2,
                }}>
                  <li><strong>Rainfall:</strong> Reduced by 25% across all districts</li>
                  <li><strong>Temperature:</strong> Increased by +2°C above baseline</li>
                  <li><strong>Test Method:</strong> Kolmogorov-Smirnov (numerical), Chi-Square (categorical)</li>
                  <li><strong>Threshold:</strong> Alert triggered when &gt;15% of features drift</li>
                  <li><strong>CI/CD:</strong> GitHub Actions auto-triggers retraining on drift</li>
                </ul>
              </div>
            </>
          )}
        </div>
      </div>
    </>
  )
}
