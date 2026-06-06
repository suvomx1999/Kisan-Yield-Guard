import { Link } from 'react-router-dom'

export default function AboutPage() {
  return (
    <>
      {/* Page Banner */}
      <div className="page-banner">
        <div className="container">
          <h1>ℹ️ About Kisan Yield Guard</h1>
          <div className="breadcrumb">
            <Link to="/">Home</Link> &nbsp;›&nbsp; About
          </div>
        </div>
      </div>

      <section className="section">
        <div className="container">
          <div className="about-content">

            {/* Main Content */}
            <div className="about-text">
              <h3>🇮🇳 The Indian Context</h3>
              <p>
                Kisan Yield Guard is tailored to the realities of Indian agriculture. 
                India's crop yields are heavily influenced by monsoon variability, regional 
                soil compositions, irrigation infrastructure, and government MSP policies. 
                Traditional statistical models fail to capture these complex, nonlinear 
                interactions across diverse agro-climatic zones.
              </p>
              <p>
                This system uses <strong>XGBoost</strong> — a state-of-the-art gradient-boosted 
                decision tree algorithm — trained on realistic synthetic data that mirrors 
                actual Indian agricultural patterns from <strong>IMD weather data</strong>, 
                <strong> CACP MSP records</strong>, and regional soil surveys.
              </p>

              <h3 style={{ marginTop: '28px' }}>🎯 Project Objectives</h3>
              <p>
                This project demonstrates a full-stack MLOps lifecycle — not just training 
                a model in a Jupyter Notebook, but building a complete production system:
              </p>
              <ul style={{ 
                paddingLeft: '20px', 
                color: 'var(--gov-text-muted)', 
                fontSize: '0.92rem', 
                lineHeight: 2.2 
              }}>
                <li>
                  <strong>End-to-End ML Engineering:</strong> Modular pipeline 
                  (preprocess → train → evaluate) with automated data scaling, 
                  encoding, and quality gating.
                </li>
                <li>
                  <strong>Production-Ready Serving:</strong> FastAPI + Docker with 
                  Pydantic schema validation to prevent garbage-in-garbage-out errors.
                </li>
                <li>
                  <strong>Automated Monitoring & Retraining:</strong> Evidently AI drift 
                  detection linked to GitHub Actions CI/CD for automatic model refresh 
                  when environmental conditions shift.
                </li>
                <li>
                  <strong>Experiment Tracking:</strong> MLflow logging of every training 
                  run with full reproducibility — metrics, parameters, artifacts, and 
                  model versioning.
                </li>
              </ul>

              <h3 style={{ marginTop: '28px' }}>🌾 Data Sources</h3>
              <p>
                While the dataset is synthetically generated for demonstration purposes, 
                it faithfully models:
              </p>
              <ul style={{ 
                paddingLeft: '20px', 
                color: 'var(--gov-text-muted)', 
                fontSize: '0.92rem', 
                lineHeight: 2.2 
              }}>
                <li>
                  <strong>IMD Weather Patterns:</strong> Realistic seasonal rainfall 
                  and temperature profiles for 16 Indian states based on India 
                  Meteorological Department climate normals.
                </li>
                <li>
                  <strong>CACP MSP Data:</strong> Real historical Minimum Support Prices 
                  (2010–2023) for Rice, Wheat, and Sugarcane as published by the 
                  Commission for Agricultural Costs & Prices.
                </li>
                <li>
                  <strong>Soil & Irrigation:</strong> State-wise soil type distributions 
                  (Alluvial, Black, Red, Laterite, Desert) and district-level irrigation 
                  coverage ranges.
                </li>
              </ul>

              <h3 style={{ marginTop: '28px' }}>📋 API Documentation</h3>
              <p>
                The FastAPI server exposes the following endpoints:
              </p>
              <div style={{ overflowX: 'auto' }}>
                <table style={{ 
                  width: '100%', 
                  borderCollapse: 'collapse', 
                  fontSize: '0.88rem',
                  marginTop: '12px',
                }}>
                  <thead>
                    <tr style={{ background: 'var(--gov-bg)', borderBottom: '2px solid var(--gov-border)' }}>
                      <th style={{ padding: '10px 14px', textAlign: 'left', fontWeight: 700, color: 'var(--navy)' }}>Method</th>
                      <th style={{ padding: '10px 14px', textAlign: 'left', fontWeight: 700, color: 'var(--navy)' }}>Endpoint</th>
                      <th style={{ padding: '10px 14px', textAlign: 'left', fontWeight: 700, color: 'var(--navy)' }}>Description</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr style={{ borderBottom: '1px solid #EDF2F7' }}>
                      <td style={{ padding: '10px 14px' }}>
                        <span style={{
                          background: 'rgba(19,136,8,0.1)',
                          color: 'var(--green)',
                          padding: '2px 8px',
                          borderRadius: '4px',
                          fontWeight: 700,
                          fontSize: '0.78rem',
                        }}>GET</span>
                      </td>
                      <td style={{ padding: '10px 14px', fontFamily: 'monospace', color: 'var(--navy)' }}>/</td>
                      <td style={{ padding: '10px 14px', color: 'var(--gov-text-muted)' }}>Health check — model status</td>
                    </tr>
                    <tr style={{ borderBottom: '1px solid #EDF2F7' }}>
                      <td style={{ padding: '10px 14px' }}>
                        <span style={{
                          background: 'rgba(255,153,51,0.1)',
                          color: 'var(--saffron-dark)',
                          padding: '2px 8px',
                          borderRadius: '4px',
                          fontWeight: 700,
                          fontSize: '0.78rem',
                        }}>POST</span>
                      </td>
                      <td style={{ padding: '10px 14px', fontFamily: 'monospace', color: 'var(--navy)' }}>/predict</td>
                      <td style={{ padding: '10px 14px', color: 'var(--gov-text-muted)' }}>Predict crop yield for district</td>
                    </tr>
                    <tr>
                      <td style={{ padding: '10px 14px' }}>
                        <span style={{
                          background: 'rgba(0,51,102,0.1)',
                          color: 'var(--navy)',
                          padding: '2px 8px',
                          borderRadius: '4px',
                          fontWeight: 700,
                          fontSize: '0.78rem',
                        }}>GET</span>
                      </td>
                      <td style={{ padding: '10px 14px', fontFamily: 'monospace', color: 'var(--navy)' }}>/drift-status</td>
                      <td style={{ padding: '10px 14px', color: 'var(--gov-text-muted)' }}>Run drift detection & return summary</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            {/* Sidebar */}
            <div className="about-sidebar">
              <div className="about-info-card">
                <h4>🏢 Project Details</h4>
                <ul>
                  <li>Project: Kisan Yield Guard</li>
                  <li>Version: 1.0.0</li>
                  <li>Language: Python 3.11</li>
                  <li>ML Model: XGBoost</li>
                  <li>License: Open Source</li>
                </ul>
              </div>

              <div className="about-info-card">
                <h4>📊 Model Parameters</h4>
                <ul>
                  <li>n_estimators: 200</li>
                  <li>max_depth: 6</li>
                  <li>learning_rate: 0.05</li>
                  <li>subsample: 0.8</li>
                  <li>colsample_bytree: 0.8</li>
                  <li>Quality Gate: R² &gt; 0.75</li>
                </ul>
              </div>

              <div className="about-info-card">
                <h4>📂 Key Files</h4>
                <ul>
                  <li>src/generate_data.py</li>
                  <li>src/preprocess.py</li>
                  <li>src/train.py</li>
                  <li>src/evaluate.py</li>
                  <li>src/drift_check.py</li>
                  <li>src/serve.py</li>
                </ul>
              </div>

              <div className="about-info-card" style={{ borderLeftColor: 'var(--green)' }}>
                <h4>🔗 External Links</h4>
                <ul>
                  <li>
                    <a href="https://github.com/suvomx1999/Kisan-Yield-Guard" 
                       target="_blank" rel="noopener"
                       style={{ color: 'var(--navy)', fontWeight: 600 }}>
                      GitHub Repository ↗
                    </a>
                  </li>
                  <li>
                    <a href="http://localhost:8000/docs" 
                       target="_blank" rel="noopener"
                       style={{ color: 'var(--navy)', fontWeight: 600 }}>
                      FastAPI Docs (Swagger) ↗
                    </a>
                  </li>
                  <li>
                    <a href="http://localhost:5000" 
                       target="_blank" rel="noopener"
                       style={{ color: 'var(--navy)', fontWeight: 600 }}>
                      MLflow UI ↗
                    </a>
                  </li>
                </ul>
              </div>
            </div>

          </div>
        </div>
      </section>
    </>
  )
}
