export function LandingPage({ onNavigate }: { onNavigate: (page: string) => void }) {
  return (
    <div className="flex h-full flex-col overflow-y-auto bg-neuro-bg p-8 text-neuro-text">
      <div className="mx-auto max-w-4xl space-y-12 pb-16">
        
        {/* Hero Section */}
        <section className="text-center space-y-6 pt-12">
          <div className="flex flex-wrap justify-center gap-3">
            <div className="inline-flex items-center gap-2 rounded-full border border-neuro-accent/30 bg-neuro-accent/10 px-4 py-1.5 text-xs font-medium text-neuro-accent">
              <span className="relative flex h-2 w-2">
                <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-neuro-accent opacity-75"></span>
                <span className="relative inline-flex h-2 w-2 rounded-full bg-neuro-accent"></span>
              </span>
              NeuroVerse v1.2 — Launch Ready
            </div>
            <div className="inline-flex items-center gap-2 rounded-full border border-teal-500/30 bg-teal-500/10 px-4 py-1.5 text-xs font-medium text-teal-400">
              ✓ Static Portfolio Active
            </div>
            <div className="inline-flex items-center gap-2 rounded-full border border-neuro-warning/30 bg-neuro-warning/10 px-4 py-1.5 text-xs font-medium text-neuro-warning">
              🔒 Closed-Loop Shadow Gated
            </div>
          </div>
          <h1 className="text-5xl font-extrabold tracking-tight text-white sm:text-6xl">
            A Safety-Gated <span className="text-neuro-accent">Research Runtime</span> & BCI Observability Platform
          </h1>
          <p className="mx-auto max-w-2xl text-lg text-neuro-muted">
            Translating offline EEG machine learning to real-time, closed-loop 3D environments. Built with a hardcoded safety gate, running explicitly in shadow-mode by default, and engineered to validate streaming systems and prevent un-gated physical feedback.
          </p>
          
          <div className="flex flex-wrap justify-center gap-4 pt-4">
            <button
              onClick={() => onNavigate('command-center')}
              className="rounded-md bg-neuro-accent px-6 py-3 font-semibold text-white transition hover:bg-neuro-accent/80 shadow-[0_0_12px_rgba(45,212,191,0.3)]"
            >
              View Command Center
            </button>
            <button
              onClick={() => onNavigate('demo')}
              className="rounded-md border border-neuro-border bg-neuro-surface px-6 py-3 font-semibold text-white transition hover:bg-neuro-border/80"
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
          <h3 className="mb-2 text-sm font-bold uppercase tracking-widest text-neuro-danger">Scientific Disclaimer & Safety Gates</h3>
          <div className="space-y-3 text-sm text-neuro-text/80">
            <p>
              NeuroVerse is an exploratory research runtime platform, not a medical or clinical device.
            </p>
            <p className="font-semibold text-neuro-danger">
              🔒 Closed-loop from real EEG is disabled by default.
            </p>
            <p>
              🧠 The corridor is not a decoded mental image. It is an adaptive scaffold driven by experimental proxy metrics.
            </p>
            <p>
              🧪 IMAGINA outputs are experimental imagery proxy artifacts, not decoded thoughts or dreams.
            </p>
            <p className="text-xs text-neuro-muted">
              Physical OpenBCI/Galea validation remains unperformed unless a real device report exists.
            </p>
          </div>
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
