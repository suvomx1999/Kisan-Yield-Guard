import { useState } from 'react'
import { NavLink } from 'react-router-dom'
import { 
  Home, BarChart3, AlertTriangle, GitBranch, Info, Menu, X 
} from 'lucide-react'

export default function NavBar() {
  const [mobileOpen, setMobileOpen] = useState(false)

  const links = [
    { to: '/', label: 'Home', icon: <Home size={15} /> },
    { to: '/predict', label: 'Yield Prediction', icon: <BarChart3 size={15} /> },
    { to: '/drift', label: 'Drift Monitoring', icon: <AlertTriangle size={15} /> },
    { to: '/pipeline', label: 'MLOps Pipeline', icon: <GitBranch size={15} /> },
    { to: '/about', label: 'About', icon: <Info size={15} /> },
  ]

  return (
    <nav className="nav-bar">
      <div className="container">
        <button 
          className="mobile-menu-btn" 
          onClick={() => setMobileOpen(!mobileOpen)}
        >
          <span>☰ Menu</span>
          {mobileOpen ? <X size={18} /> : <Menu size={18} />}
        </button>
        <div className={`nav-links ${mobileOpen ? 'open' : ''}`}>
          {links.map(link => (
            <NavLink
              key={link.to}
              to={link.to}
              end={link.to === '/'}
              className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
              onClick={() => setMobileOpen(false)}
            >
              {link.icon}
              {link.label}
            </NavLink>
          ))}
        </div>
      </div>
    </nav>
  )
}
