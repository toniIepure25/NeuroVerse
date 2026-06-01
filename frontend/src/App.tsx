import { useState, lazy, Suspense } from 'react'

const LandingPage = lazy(() => import('./components/Pages/LandingPage').then(m => ({ default: m.LandingPage })))
const EvidenceCenter = lazy(() => import('./components/Pages/EvidenceCenter').then(m => ({ default: m.EvidenceCenter })))
const HiringPage = lazy(() => import('./components/Pages/HiringPage').then(m => ({ default: m.HiringPage })))
const ProtocolCenter = lazy(() => import('./components/Pages/ProtocolCenter').then(m => ({ default: m.ProtocolCenter })))
const DataSourceWizard = lazy(() => import('./components/Pages/DataSourceWizard').then(m => ({ default: m.DataSourceWizard })))
const CommandCenter = lazy(() => import('./components/Pages/CommandCenter').then(m => ({ default: m.CommandCenter })))
const AppShell = lazy(() => import('./components/Layout/AppShell').then(m => ({ default: m.AppShell })))

export default function App() {
  const [currentPage, setCurrentPage] = useState<string>('landing')

  const renderPage = () => {
    switch (currentPage) {
      case 'command-center':
        return <CommandCenter onNavigate={setCurrentPage} />
      case 'demo':
        return <AppShell />
      case 'evidence':
        return <EvidenceCenter />
      case 'hiring':
        return <HiringPage />
      case 'protocols':
        return <ProtocolCenter />
      case 'data-sources':
        return <DataSourceWizard onNavigate={setCurrentPage} />
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
        
        <nav className="flex flex-wrap justify-end gap-x-6 gap-y-2 text-sm font-medium">
          <button 
            onClick={() => setCurrentPage('landing')} 
            className={`transition ${currentPage === 'landing' ? 'text-neuro-accent' : 'text-neuro-muted hover:text-neuro-text'}`}
          >
            Overview
          </button>
          <button 
            onClick={() => setCurrentPage('command-center')} 
            className={`transition ${currentPage === 'command-center' ? 'text-neuro-accent' : 'text-neuro-muted hover:text-neuro-text'}`}
          >
            Command Center
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
            onClick={() => setCurrentPage('protocols')}
            className={`transition ${currentPage === 'protocols' ? 'text-neuro-accent' : 'text-neuro-muted hover:text-neuro-text'}`}
          >
            Protocol Center
          </button>
          <button
            onClick={() => setCurrentPage('data-sources')}
            className={`transition ${currentPage === 'data-sources' ? 'text-neuro-accent' : 'text-neuro-muted hover:text-neuro-text'}`}
          >
            Data Sources
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
        <Suspense fallback={
          <div className="flex h-full w-full items-center justify-center bg-neuro-bg/50 backdrop-blur-md">
            <div className="flex flex-col items-center gap-4">
              <div className="h-10 w-10 animate-spin rounded-full border-4 border-neuro-accent/20 border-t-neuro-accent" />
              <div className="text-xs font-mono tracking-widest uppercase text-neuro-accent animate-pulse">Hydrating Component...</div>
            </div>
          </div>
        }>
          {renderPage()}
        </Suspense>
      </div>
    </div>
  )
}
