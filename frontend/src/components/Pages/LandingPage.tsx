export function LandingPage({ onNavigate }: { onNavigate: (page: string) => void }) {
  return (
    <div className="flex h-full flex-col overflow-y-auto bg-neuro-bg p-8 text-neuro-text">
      <div className="mx-auto max-w-4xl space-y-12 pb-16">
        
        {/* Hero Section */}
        <section className="text-center space-y-6 pt-12">
          <div className="inline-flex items-center gap-2 rounded-full border border-neuro-accent/30 bg-neuro-accent/10 px-4 py-1.5 text-xs font-medium text-neuro-accent">
            <span className="relative flex h-2 w-2">
              <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-neuro-accent opacity-75"></span>
              <span className="relative inline-flex h-2 w-2 rounded-full bg-neuro-accent"></span>
            </span>
            NeuroVerse v1.1 — Release Candidate
          </div>
          <h1 className="text-5xl font-extrabold tracking-tight text-white sm:text-6xl">
            A Safety-Gated <span className="text-neuro-accent">Neuroadaptive</span> Interface
          </h1>
          <p className="mx-auto max-w-2xl text-lg text-neuro-muted">
            Translating offline EEG machine learning to real-time, closed-loop 3D environments. Built for rigor, explicitly shadow-only by default, and engineered to highlight the gap between dataset accuracy and live inference.
          </p>
          
          <div className="flex justify-center gap-4 pt-4">
            <button
              onClick={() => onNavigate('demo')}
              className="rounded-md bg-neuro-accent px-6 py-3 font-semibold text-white transition hover:bg-neuro-accent/80"
            >
              Enter Dream Corridor
            </button>
            <button
              onClick={() => onNavigate('evidence')}
              className="rounded-md border border-neuro-border bg-neuro-surface px-6 py-3 font-semibold text-white transition hover:bg-neuro-border/80"
            >
              View Evidence Center
            </button>
          </div>
        </section>

        {/* Scientific Honesty Disclaimer */}
        <section className="rounded-lg border border-neuro-danger/30 bg-neuro-danger/5 p-6 text-center">
          <h3 className="mb-2 text-sm font-bold uppercase tracking-widest text-neuro-danger">Scientific Disclaimer</h3>
          <p className="text-sm text-neuro-text/80">
            NeuroVerse is not a medical device. It does not read thoughts, decode dreams, or detect consciousness. 
            The corridor is an adaptive scaffold driven by experimental proxy metrics. Event-locked EEG classifiers predict controlled dataset task labels under experimental conditions; they should not be interpreted as general mind-reading models. Physical hardware (OpenBCI/Galea) remains unvalidated unless a real physical device report is present.
          </p>
        </section>

        {/* What it is / is not */}
        <section className="grid grid-cols-1 gap-8 md:grid-cols-2">
          <div className="rounded-lg border border-neuro-border bg-neuro-surface p-6">
            <h3 className="mb-4 text-xl font-bold text-white">What NeuroVerse Is</h3>
            <ul className="space-y-3 text-sm text-neuro-muted">
              <li className="flex items-start gap-2">
                <span className="text-neuro-accent">✓</span>
                A real-time FastAPI + React WebSocket architecture.
              </li>
              <li className="flex items-start gap-2">
                <span className="text-neuro-accent">✓</span>
                A pipeline for evaluating offline classical ML (CSP/FBCSP) on public datasets (PhysioNet).
              </li>
              <li className="flex items-start gap-2">
                <span className="text-neuro-accent">✓</span>
                A continuous Lab Streaming Layer (LSL) receiver that validates jitter and drift.
              </li>
              <li className="flex items-start gap-2">
                <span className="text-neuro-accent">✓</span>
                A safety-first system that defaults to "shadow mode" to prevent unvalidated adaptations.
              </li>
            </ul>
          </div>
          <div className="rounded-lg border border-neuro-border bg-neuro-surface p-6">
            <h3 className="mb-4 text-xl font-bold text-white">What It Is Not</h3>
            <ul className="space-y-3 text-sm text-neuro-muted">
              <li className="flex items-start gap-2">
                <span className="text-neuro-danger">✗</span>
                A plug-and-play thought decoder.
              </li>
              <li className="flex items-start gap-2">
                <span className="text-neuro-danger">✗</span>
                A tool for clinical diagnosis or therapy.
              </li>
              <li className="flex items-start gap-2">
                <span className="text-neuro-danger">✗</span>
                A fully validated physical hardware application (yet).
              </li>
              <li className="flex items-start gap-2">
                <span className="text-neuro-danger">✗</span>
                An un-gated, unsafe real-time control system.
              </li>
            </ul>
          </div>
        </section>

        {/* Architecture summary */}
        <section className="rounded-lg border border-neuro-border bg-neuro-surface p-6">
          <h3 className="mb-4 text-xl font-bold text-white text-center">Architecture Overview</h3>
          <div className="flex flex-col items-center space-y-4 font-mono text-xs text-neuro-muted">
            <div className="rounded border border-neuro-border bg-neuro-bg p-3 text-center w-full max-w-md">
              Simulated Biosignals / Dataset Replay / LSL Stream
            </div>
            <div className="text-neuro-accent">↓</div>
            <div className="rounded border border-neuro-border bg-neuro-bg p-3 text-center w-full max-w-md">
              Preprocessing (Bandpass, CSP filtering, epoching)
            </div>
            <div className="text-neuro-accent">↓</div>
            <div className="rounded border border-neuro-border bg-neuro-bg p-3 text-center w-full max-w-md">
              State Estimation (Heuristic or Classical ML)
            </div>
            <div className="text-neuro-accent">↓</div>
            <div className="rounded border border-neuro-danger/50 bg-neuro-danger/10 p-3 text-center w-full max-w-md border-dashed">
              Safety Gate (Shadow Mode / Blocks Uncertain Signals)
            </div>
            <div className="text-neuro-accent">↓</div>
            <div className="rounded border border-neuro-border bg-neuro-bg p-3 text-center w-full max-w-md">
              FastAPI WebSocket → React Three Fiber Frontend
            </div>
          </div>
        </section>

      </div>
    </div>
  )
}
