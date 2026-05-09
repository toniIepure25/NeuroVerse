import { useState } from 'react'
import { AppShell } from './components/Layout/AppShell'
import { LandingPage } from './components/Pages/LandingPage'
import { EvidenceCenter } from './components/Pages/EvidenceCenter'
import { HiringPage } from './components/Pages/HiringPage'

export default function App() {
  const [currentPage, setCurrentPage] = useState<string>('landing')

  const renderPage = () => {
    switch (currentPage) {
      case 'demo':
        return <AppShell />
      case 'evidence':
        return <EvidenceCenter />
      case 'hiring':
        return <HiringPage />
      case 'landing':
      default:
        return <LandingPage onNavigate={setCurrentPage} />
    }
  }

  return (
    <div className="flex h-screen w-screen flex-col overflow-hidden bg-neuro-bg text-neuro-text">
      {/* Global Navigation Header */}
      <header className="flex shrink-0 items-center justify-between border-b border-neuro-border px-6 py-3 bg-neuro-surface/50">
        <div className="flex items-center gap-3 cursor-pointer" onClick={() => setCurrentPage('landing')}>
          <div className="h-3 w-3 rounded-full bg-neuro-accent shadow-[0_0_8px_rgba(45,212,191,0.5)]" />
          <h1 className="text-lg font-semibold tracking-tight">NeuroVerse</h1>
        </div>
        
        <nav className="flex gap-6 text-sm font-medium">
          <button 
            onClick={() => setCurrentPage('landing')} 
            className={`transition ${currentPage === 'landing' ? 'text-neuro-accent' : 'text-neuro-muted hover:text-neuro-text'}`}
          >
            Overview
          </button>
          <button 
            onClick={() => setCurrentPage('demo')} 
            className={`transition ${currentPage === 'demo' ? 'text-neuro-accent' : 'text-neuro-muted hover:text-neuro-text'}`}
          >
            Dream Corridor
          </button>
          <button 
            onClick={() => setCurrentPage('evidence')} 
            className={`transition ${currentPage === 'evidence' ? 'text-neuro-accent' : 'text-neuro-muted hover:text-neuro-text'}`}
          >
            Evidence Center
          </button>
          <button 
            onClick={() => setCurrentPage('hiring')} 
            className={`transition ${currentPage === 'hiring' ? 'text-neuro-accent' : 'text-neuro-muted hover:text-neuro-text'}`}
          >
            Hiring / Interview
          </button>
        </nav>
      </header>

      <div className="flex min-h-0 flex-1">
        {renderPage()}
      </div>
    </div>
  )
}
