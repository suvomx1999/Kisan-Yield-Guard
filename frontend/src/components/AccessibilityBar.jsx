import { useState } from 'react'

export default function AccessibilityBar() {
  const [lang, setLang] = useState('en')

  const changeFontSize = (delta) => {
    const root = document.documentElement
    const current = parseFloat(getComputedStyle(root).fontSize)
    root.style.fontSize = Math.min(22, Math.max(12, current + delta)) + 'px'
  }

  return (
    <div className="accessibility-bar">
      <div className="container">
        <div className="left-links">
          <a href="#main-content">Skip to Main Content</a>
          <span style={{ opacity: 0.4 }}>|</span>
          <a href="/sitemap">Screen Reader Access</a>
        </div>
        <div className="right-controls">
          <div className="font-size-controls">
            <button onClick={() => changeFontSize(-1)} title="Decrease font size">A-</button>
            <button onClick={() => changeFontSize(0)} title="Default font size">A</button>
            <button onClick={() => changeFontSize(1)} title="Increase font size">A+</button>
          </div>
          <div className="lang-toggle">
            <button 
              className={lang === 'en' ? 'active' : ''} 
              onClick={() => setLang('en')}
            >
              English
            </button>
            <button 
              className={lang === 'hi' ? 'active' : ''} 
              onClick={() => setLang('hi')}
            >
              हिन्दी
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
