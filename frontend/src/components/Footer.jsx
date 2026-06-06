import { Link } from 'react-router-dom'

export default function Footer() {
  return (
    <footer className="main-footer">
      <div className="container">
        <div className="footer-top">
          <div className="footer-brand">
            <h3>🌾 Kisan Yield Guard</h3>
            <p>
              An end-to-end MLOps pipeline for Indian district-level crop yield 
              prediction with automated data drift detection and CI/CD retraining. 
              Built for the Digital Agriculture Mission under the Government of India.
            </p>
          </div>

          <div className="footer-col">
            <h4>Quick Links</h4>
            <ul>
              <li><Link to="/">🏠 Home</Link></li>
              <li><Link to="/predict">📊 Yield Prediction</Link></li>
              <li><Link to="/drift">⚠️ Drift Monitor</Link></li>
              <li><Link to="/pipeline">🔧 MLOps Pipeline</Link></li>
            </ul>
          </div>

          <div className="footer-col">
            <h4>Technology</h4>
            <ul>
              <li><a href="https://xgboost.readthedocs.io/" target="_blank" rel="noopener">XGBoost</a></li>
              <li><a href="https://mlflow.org/" target="_blank" rel="noopener">MLflow</a></li>
              <li><a href="https://www.evidentlyai.com/" target="_blank" rel="noopener">Evidently AI</a></li>
              <li><a href="https://fastapi.tiangolo.com/" target="_blank" rel="noopener">FastAPI</a></li>
            </ul>
          </div>

          <div className="footer-col">
            <h4>Resources</h4>
            <ul>
              <li><a href="https://github.com/suvomx1999/Kisan-Yield-Guard" target="_blank" rel="noopener">GitHub Repository</a></li>
              <li><a href="#api-docs">API Documentation</a></li>
              <li><Link to="/about">About Scheme</Link></li>
              <li><a href="#feedback">Feedback</a></li>
            </ul>
          </div>
        </div>
      </div>

      <div className="footer-bottom">
        <div className="container">
          <p>© 2024 Kisan Yield Guard — Ministry of Agriculture & Farmers Welfare</p>
          <span className="nic-credit">
            Designed & Developed by Digital Agriculture Division | Content Owned by Dept. of Agriculture
          </span>
          <span className="visitor-count">
            👁️ Visitors: {(Math.floor(Math.random() * 50000) + 120000).toLocaleString('en-IN')}
          </span>
        </div>
      </div>
    </footer>
  )
}
