import { Link } from 'react-router-dom'

const STEPS = [
  {
    num: 1,
    title: 'Data Generation',
    desc: 'Synthetic Indian agricultural dataset with 5,000+ records covering 16 states, 30 districts, real IMD weather patterns, CACP MSP data (2010–2023), and regional soil correlations.',
    tags: ['Python', 'NumPy', 'Pandas'],
    color: '#FF9933',
    file: 'generate_data.py',
  },
  {
    num: 2,
    title: 'Preprocessing Pipeline',
    desc: 'Scales numerical features (rainfall, temperature, irrigation, fertilizer, MSP) with StandardScaler. Encodes categoricals (crop, season, state, district, soil) with LabelEncoder. Saves artifacts as joblib.',
    tags: ['scikit-learn', 'StandardScaler', 'LabelEncoder'],
    color: '#003366',
    file: 'preprocess.py',
  },
  {
    num: 3,
    title: 'XGBoost Training',
    desc: 'Trains a gradient-boosted decision tree with 200 estimators, max_depth=6, learning_rate=0.05. Logs all metrics (RMSE, MAE, R²), hyperparameters, and feature importance plots to MLflow.',
    tags: ['XGBoost', 'MLflow', 'Tracking URI'],
    color: '#138808',
    file: 'train.py',
  },
  {
    num: 4,
    title: 'Evaluation & Quality Gates',
    desc: 'Evaluates the trained model on the held-out test set. If R² > 0.75, the model passes the quality gate and is promoted to the MLflow Model Registry at Production stage.',
    tags: ['R² > 0.75', 'RMSE', 'MAE', 'MLflow Registry'],
    color: '#FF9933',
    file: 'evaluate.py',
  },
  {
    num: 5,
    title: 'MLflow Model Registry',
    desc: 'The registered KisanYieldModel is versioned and managed through Staging → Production stages. The FastAPI server loads the latest Production model at startup.',
    tags: ['MLflow', 'Model Versioning', 'Production Stage'],
    color: '#003366',
    file: 'mlruns/',
  },
  {
    num: 6,
    title: 'Evidently AI Drift Detection',
    desc: 'Compares reference baseline against incoming data using KS-test and Chi-Square. Simulates drought (−25% rain, +2°C temp). Triggers retraining if >15% features drift.',
    tags: ['Evidently AI', 'KS Test', 'Chi-Square'],
    color: '#138808',
    file: 'drift_check.py',
  },
  {
    num: 7,
    title: 'FastAPI Serving Endpoint',
    desc: 'Production REST API with Pydantic validation. Exposes /predict (POST), / (health check), and /drift-status (GET). Returns yield prediction with category and model metadata.',
    tags: ['FastAPI', 'Uvicorn', 'Pydantic', 'Docker'],
    color: '#FF9933',
    file: 'serve.py',
  },
  {
    num: 8,
    title: 'GitHub Actions CI/CD',
    desc: 'Automated quarterly workflow that runs drift detection. If drift is detected, it triggers full pipeline retraining, model re-evaluation, registry update, and Evidently HTML report upload.',
    tags: ['GitHub Actions', 'CI/CD', 'Auto-Retrain'],
    color: '#003366',
    file: '.github/workflows/retrain.yml',
  },
]

export default function PipelinePage() {
  return (
    <>
      {/* Page Banner */}
      <div className="page-banner">
        <div className="container">
          <h1>🔧 MLOps Pipeline Architecture</h1>
          <div className="breadcrumb">
            <Link to="/">Home</Link> &nbsp;›&nbsp; Pipeline
          </div>
        </div>
      </div>

      <section className="section">
        <div className="container">
          <div className="section-header">
            <div className="hindi-label">पाइपलाइन वास्तुकला</div>
            <h2>End-to-End ML Pipeline</h2>
            <p>
              From data generation to automated retraining — 8 stages of production-grade MLOps
            </p>
          </div>

          <div className="pipeline-flow">
            {STEPS.map((step, idx) => (
              <div className="pipeline-step" key={step.num}>
                <div className="pipeline-connector">
                  <div className="pipeline-dot" style={{ background: step.color }}>
                    {step.num}
                  </div>
                  {idx < STEPS.length - 1 && (
                    <div className="pipeline-line" style={{ background: `linear-gradient(${step.color}, ${STEPS[idx+1].color})` }} />
                  )}
                </div>
                <div className="pipeline-step-content">
                  <h3>{step.title}</h3>
                  <p>{step.desc}</p>
                  <div className="tech-tags">
                    {step.tags.map(t => (
                      <span className="tech-tag" key={t}>{t}</span>
                    ))}
                    <span className="tech-tag" style={{
                      background: 'rgba(255,153,51,0.1)',
                      borderColor: 'rgba(255,153,51,0.3)',
                      color: 'var(--saffron-dark)',
                    }}>
                      📄 {step.file}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Tech Stack Table */}
          <div style={{ marginTop: '48px' }}>
            <div className="section-header">
              <div className="hindi-label">प्रौद्योगिकी स्टैक</div>
              <h2>Technology Stack</h2>
            </div>

            <div style={{
              background: 'white',
              borderRadius: 'var(--radius-md)',
              overflow: 'hidden',
              boxShadow: 'var(--shadow-sm)',
              border: '1px solid var(--gov-border)',
              maxWidth: '700px',
              margin: '0 auto',
            }}>
              <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                <thead>
                  <tr style={{
                    background: 'linear-gradient(135deg, var(--navy), var(--navy-dark))',
                    color: 'white',
                  }}>
                    <th style={{ padding: '14px 20px', textAlign: 'left', fontSize: '0.85rem', fontWeight: 600 }}>Component</th>
                    <th style={{ padding: '14px 20px', textAlign: 'left', fontSize: '0.85rem', fontWeight: 600 }}>Technology</th>
                  </tr>
                </thead>
                <tbody>
                  {[
                    ['Language', 'Python 3.11'],
                    ['Machine Learning', 'XGBoost, scikit-learn'],
                    ['Experiment Tracking', 'MLflow'],
                    ['Drift Detection', 'Evidently AI'],
                    ['Model Serving', 'FastAPI, Uvicorn, Pydantic'],
                    ['CI/CD & Automation', 'GitHub Actions'],
                    ['Containerization', 'Docker'],
                    ['Cloud Deployment', 'Render'],
                    ['Frontend', 'React + Vite'],
                  ].map(([comp, tech], i) => (
                    <tr key={comp} style={{
                      background: i % 2 === 0 ? '#FAFBFC' : 'white',
                      borderBottom: '1px solid #EDF2F7',
                    }}>
                      <td style={{ padding: '12px 20px', fontSize: '0.88rem', fontWeight: 600, color: 'var(--navy)' }}>{comp}</td>
                      <td style={{ padding: '12px 20px', fontSize: '0.88rem', color: 'var(--gov-text-muted)' }}>{tech}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

        </div>
      </section>
    </>
  )
}
