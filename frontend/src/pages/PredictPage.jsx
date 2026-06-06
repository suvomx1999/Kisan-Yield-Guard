import { useState } from 'react'
import { Link } from 'react-router-dom'
import { BarChart3, Send, RotateCcw, Loader2 } from 'lucide-react'

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const DISTRICTS_BY_STATE = {
  'Punjab': ['Ludhiana', 'Amritsar', 'Patiala'],
  'Haryana': ['Karnal', 'Hisar'],
  'Uttar Pradesh': ['Lucknow', 'Meerut', 'Gorakhpur'],
  'Bihar': ['Patna', 'Muzaffarpur'],
  'West Bengal': ['Bardhaman', 'Hooghly'],
  'Maharashtra': ['Nashik', 'Pune', 'Kolhapur'],
  'Andhra Pradesh': ['Guntur', 'Krishna'],
  'Tamil Nadu': ['Coimbatore', 'Thanjavur'],
  'Karnataka': ['Belgaum', 'Mysore'],
  'Madhya Pradesh': ['Indore', 'Jabalpur'],
  'Rajasthan': ['Jaipur', 'Jodhpur'],
  'Odisha': ['Cuttack'],
  'Chhattisgarh': ['Raipur'],
  'Telangana': ['Warangal'],
  'Gujarat': ['Ahmedabad'],
  'Assam': ['Nagaon'],
}

const CROP_SEASONS = {
  'Rice': ['Kharif'],
  'Wheat': ['Rabi'],
  'Sugarcane': ['Kharif', 'Zaid'],
}

const SOIL_TYPES = ['Alluvial', 'Black', 'Red', 'Laterite', 'Desert']

const DEFAULT_FORM = {
  state: '',
  district: '',
  crop: '',
  year: 2024,
  season: '',
  rainfall_mm: '',
  temperature_avg_c: '',
  soil_type: '',
  irrigation_pct: '',
  fertilizer_kg_per_ha: '',
  msp_inr_per_quintal: '',
}

export default function PredictPage() {
  const [form, setForm] = useState(DEFAULT_FORM)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const districts = form.state ? (DISTRICTS_BY_STATE[form.state] || []) : []
  const seasons = form.crop ? (CROP_SEASONS[form.crop] || []) : []

  const handleChange = (e) => {
    const { name, value } = e.target
    const updates = { [name]: value }

    // Reset dependent fields
    if (name === 'state') {
      updates.district = ''
    }
    if (name === 'crop') {
      updates.season = ''
      // Auto-fill season if single option
      const s = CROP_SEASONS[value]
      if (s && s.length === 1) updates.season = s[0]
    }

    setForm(prev => ({ ...prev, ...updates }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResult(null)

    const payload = {
      ...form,
      year: parseInt(form.year),
      rainfall_mm: parseFloat(form.rainfall_mm),
      temperature_avg_c: parseFloat(form.temperature_avg_c),
      irrigation_pct: parseFloat(form.irrigation_pct),
      fertilizer_kg_per_ha: parseFloat(form.fertilizer_kg_per_ha),
      msp_inr_per_quintal: parseFloat(form.msp_inr_per_quintal),
    }

    try {
      const res = await fetch(`${API_BASE}/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      })

      if (!res.ok) {
        const err = await res.json()
        throw new Error(err.detail || `HTTP ${res.status}`)
      }

      const data = await res.json()
      setResult(data)
    } catch (err) {
      setError(err.message || 'Failed to connect to the API. Ensure the FastAPI server is running on port 8000.')
    } finally {
      setLoading(false)
    }
  }

  const handleReset = () => {
    setForm(DEFAULT_FORM)
    setResult(null)
    setError(null)
  }

  return (
    <>
      {/* Page Banner */}
      <div className="page-banner">
        <div className="container">
          <h1>📊 Crop Yield Prediction</h1>
          <div className="breadcrumb">
            <Link to="/">Home</Link> &nbsp;›&nbsp; Yield Prediction
          </div>
        </div>
      </div>

      {/* Form Section */}
      <div className="form-page">
        <div className="container">
          <div className="form-layout">

            {/* ── Prediction Form ──────────────────────────── */}
            <div className="form-card">
              <div className="form-card-header">
                <BarChart3 size={22} />
                <h2>Enter Agricultural Parameters</h2>
              </div>
              <div className="form-card-body">
                {error && (
                  <div className="error-toast">
                    ⚠️ {error}
                  </div>
                )}

                <form onSubmit={handleSubmit}>
                  <div className="form-grid">

                    {/* Location Section */}
                    <div className="form-divider">
                      <span>📍 Location Details</span>
                    </div>

                    <div className="form-group">
                      <label>State <span className="required">*</span></label>
                      <select name="state" value={form.state} onChange={handleChange} required>
                        <option value="">-- Select State --</option>
                        {Object.keys(DISTRICTS_BY_STATE).map(st => (
                          <option key={st} value={st}>{st}</option>
                        ))}
                      </select>
                    </div>

                    <div className="form-group">
                      <label>District <span className="required">*</span></label>
                      <select name="district" value={form.district} onChange={handleChange} required disabled={!form.state}>
                        <option value="">-- Select District --</option>
                        {districts.map(d => (
                          <option key={d} value={d}>{d}</option>
                        ))}
                      </select>
                    </div>

                    {/* Crop Section */}
                    <div className="form-divider">
                      <span>🌾 Crop Information</span>
                    </div>

                    <div className="form-group">
                      <label>Crop <span className="required">*</span></label>
                      <select name="crop" value={form.crop} onChange={handleChange} required>
                        <option value="">-- Select Crop --</option>
                        <option value="Rice">Rice (धान)</option>
                        <option value="Wheat">Wheat (गेहूं)</option>
                        <option value="Sugarcane">Sugarcane (गन्ना)</option>
                      </select>
                    </div>

                    <div className="form-group">
                      <label>Season <span className="required">*</span></label>
                      <select name="season" value={form.season} onChange={handleChange} required disabled={!form.crop}>
                        <option value="">-- Select Season --</option>
                        {seasons.map(s => (
                          <option key={s} value={s}>{s}</option>
                        ))}
                      </select>
                    </div>

                    <div className="form-group">
                      <label>Year <span className="required">*</span></label>
                      <input
                        type="number"
                        name="year"
                        value={form.year}
                        onChange={handleChange}
                        min="2010"
                        max="2030"
                        required
                      />
                    </div>

                    <div className="form-group">
                      <label>Soil Type <span className="required">*</span></label>
                      <select name="soil_type" value={form.soil_type} onChange={handleChange} required>
                        <option value="">-- Select Soil Type --</option>
                        {SOIL_TYPES.map(s => (
                          <option key={s} value={s}>{s}</option>
                        ))}
                      </select>
                    </div>

                    {/* Weather Section */}
                    <div className="form-divider">
                      <span>🌧️ Weather & Environment</span>
                    </div>

                    <div className="form-group">
                      <label>Rainfall (mm) <span className="required">*</span></label>
                      <input
                        type="number"
                        name="rainfall_mm"
                        value={form.rainfall_mm}
                        onChange={handleChange}
                        placeholder="e.g. 850"
                        min="0"
                        step="0.1"
                        required
                      />
                    </div>

                    <div className="form-group">
                      <label>Avg Temperature (°C) <span className="required">*</span></label>
                      <input
                        type="number"
                        name="temperature_avg_c"
                        value={form.temperature_avg_c}
                        onChange={handleChange}
                        placeholder="e.g. 27.5"
                        min="0"
                        max="50"
                        step="0.1"
                        required
                      />
                    </div>

                    <div className="form-group">
                      <label>Irrigation Coverage (%) <span className="required">*</span></label>
                      <input
                        type="number"
                        name="irrigation_pct"
                        value={form.irrigation_pct}
                        onChange={handleChange}
                        placeholder="e.g. 75"
                        min="0"
                        max="100"
                        step="0.1"
                        required
                      />
                    </div>

                    <div className="form-group">
                      <label>Fertilizer (kg/ha) <span className="required">*</span></label>
                      <input
                        type="number"
                        name="fertilizer_kg_per_ha"
                        value={form.fertilizer_kg_per_ha}
                        onChange={handleChange}
                        placeholder="e.g. 180"
                        min="0"
                        step="0.1"
                        required
                      />
                    </div>

                    {/* Economics Section */}
                    <div className="form-divider">
                      <span>💰 MSP Data</span>
                    </div>

                    <div className="form-group full-width">
                      <label>MSP (₹ per Quintal) <span className="required">*</span></label>
                      <input
                        type="number"
                        name="msp_inr_per_quintal"
                        value={form.msp_inr_per_quintal}
                        onChange={handleChange}
                        placeholder="e.g. 2275 (Source: CACP)"
                        min="0"
                        step="1"
                        required
                      />
                    </div>

                    {/* Actions */}
                    <div className="form-actions">
                      <button type="submit" className="btn btn-green btn-lg" disabled={loading}>
                        {loading ? (
                          <>
                            <Loader2 size={18} className="spinning" style={{ animation: 'spin 0.8s linear infinite' }} />
                            Processing...
                          </>
                        ) : (
                          <>
                            <Send size={18} />
                            Submit Prediction
                          </>
                        )}
                      </button>
                      <button type="button" className="btn btn-outline" onClick={handleReset}>
                        <RotateCcw size={16} />
                        Reset Form
                      </button>
                    </div>

                  </div>
                </form>
              </div>
            </div>

            {/* ── Result Sidebar ───────────────────────────── */}
            <div className="result-sidebar">
              <div className="result-card">
                <div className="result-card-header">
                  <h3>🌾 Prediction Result</h3>
                </div>
                <div className="result-card-body">
                  {!result && !loading && (
                    <div className="result-placeholder">
                      <div className="placeholder-icon">📋</div>
                      <p>
                        Fill in the agricultural parameters and click 
                        <strong> "Submit Prediction"</strong> to see the AI-predicted crop yield for your district.
                      </p>
                    </div>
                  )}

                  {loading && (
                    <div className="loading-spinner">
                      <div className="spinner" />
                    </div>
                  )}

                  {result && (
                    <div className="result-data">
                      <div className="result-yield">
                        <div className="yield-value">
                          {result.predicted_yield_kg_per_ha.toLocaleString('en-IN')}
                        </div>
                        <div className="yield-unit">kg per hectare</div>
                        <span className={`yield-badge ${result.yield_category.toLowerCase()}`}>
                          {result.yield_category} Yield
                        </span>
                      </div>

                      <div className="result-meta">
                        <div className="result-meta-item">
                          <span className="label">District</span>
                          <span className="value">{result.district}</span>
                        </div>
                        <div className="result-meta-item">
                          <span className="label">Crop</span>
                          <span className="value">{result.crop}</span>
                        </div>
                        <div className="result-meta-item">
                          <span className="label">Category</span>
                          <span className="value" style={{
                            color: result.yield_category === 'High' ? 'var(--green)' :
                                   result.yield_category === 'Medium' ? 'var(--saffron-dark)' :
                                   'var(--gov-red)'
                          }}>
                            {result.yield_category}
                          </span>
                        </div>
                        <div className="result-meta-item">
                          <span className="label">Model</span>
                          <span className="value" style={{ fontSize: '0.75rem' }}>
                            {result.confidence_note}
                          </span>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              </div>

              {/* Quick Tips Card */}
              <div style={{
                background: 'white',
                borderRadius: 'var(--radius-md)',
                padding: '20px',
                marginTop: '16px',
                boxShadow: 'var(--shadow-sm)',
                border: '1px solid var(--gov-border)',
                borderLeft: '4px solid var(--saffron)',
              }}>
                <h4 style={{ fontSize: '0.88rem', color: 'var(--navy)', marginBottom: '10px', fontWeight: 700 }}>
                  💡 Helpful Tips
                </h4>
                <ul style={{ listStyle: 'none', padding: 0, fontSize: '0.8rem', color: 'var(--gov-text-muted)', lineHeight: 1.7 }}>
                  <li>▸ MSP values are sourced from CACP data (2010–2023)</li>
                  <li>▸ Rice is a Kharif crop, Wheat is Rabi</li>
                  <li>▸ Punjab/Haryana have highest irrigation (%)</li>
                  <li>▸ Alluvial soil suits Rice & Wheat best</li>
                  <li>▸ Sugarcane yields are measured in 40K–90K range</li>
                </ul>
              </div>
            </div>

          </div>
        </div>
      </div>
    </>
  )
}
