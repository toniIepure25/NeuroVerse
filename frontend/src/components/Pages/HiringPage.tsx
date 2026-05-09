export function HiringPage() {
  return (
    <div className="flex h-full flex-col overflow-y-auto bg-neuro-bg p-8 text-neuro-text">
      <div className="mx-auto max-w-4xl space-y-12 pb-16">
        
        <header className="space-y-4">
          <h1 className="text-4xl font-extrabold tracking-tight text-white">Why This Matters for Neurotech Roles</h1>
          <p className="max-w-3xl text-lg text-neuro-muted">
            NeuroVerse is designed as a fully executable, transparent portfolio piece that demonstrates end-to-end BCI systems engineering.
          </p>
        </header>

        <section className="grid grid-cols-1 md:grid-cols-2 gap-8">
          
          <div className="rounded-lg border border-neuro-border bg-neuro-surface p-6">
            <h3 className="mb-4 text-xl font-bold text-white">The 90-Second Pitch</h3>
            <p className="text-sm text-neuro-text/90 italic border-l-2 border-neuro-accent pl-4">
              "NeuroVerse is a fully integrated, real-time closed-loop Brain-Computer Interface research platform. I built it to validate the entire neuroadaptive pipeline—from signal acquisition and classical ML modeling on public datasets to a React Three Fiber visual interface. It acts as an executable portfolio piece demonstrating rigorous software engineering, data streaming (LSL), and a stringent safety-first approach to physical hardware integration."
            </p>
          </div>

          <div className="rounded-lg border border-neuro-border bg-neuro-surface p-6">
            <h3 className="mb-4 text-xl font-bold text-white">Skills Demonstrated</h3>
            <ul className="space-y-2 text-sm text-neuro-muted">
              <li className="flex items-center gap-2"><span className="text-neuro-accent">•</span> BCI Signal Processing (Filtering, Epoching, CSP)</li>
              <li className="flex items-center gap-2"><span className="text-neuro-accent">•</span> EEG Machine Learning (FBCSP, Data Leakage Prevention)</li>
              <li className="flex items-center gap-2"><span className="text-neuro-accent">•</span> Real-time Systems (FastAPI, WebSockets, Asyncio)</li>
              <li className="flex items-center gap-2"><span className="text-neuro-accent">•</span> Data Streaming (LSL, pyxdf, BrainFlow)</li>
              <li className="flex items-center gap-2"><span className="text-neuro-accent">•</span> Safety Engineering (Shadow mode, SQI gating)</li>
              <li className="flex items-center gap-2"><span className="text-neuro-accent">•</span> Product & UI (React, Three.js, Typescript)</li>
            </ul>
          </div>
          
        </section>

        <section className="rounded-lg border border-neuro-border bg-neuro-surface p-6">
          <h2 className="mb-4 text-2xl font-bold text-white">Questions I Expect</h2>
          
          <div className="space-y-6">
            <div>
              <h4 className="font-bold text-white text-sm mb-1">Q: Why are the LOSO metrics so modest?</h4>
              <p className="text-sm text-neuro-muted">
                <strong>A:</strong> Scientific honesty. EEG signals are highly non-stationary. A model trained on a group of subjects will often overfit to subject-specific features. LOSO forces the model to predict on a completely unseen brain, resulting in a performance drop that accurately reflects real-world zero-shot BCI deployment challenges.
              </p>
            </div>
            
            <div>
              <h4 className="font-bold text-white text-sm mb-1">Q: Why use classical ML (CSP) over Deep Learning?</h4>
              <p className="text-sm text-neuro-muted">
                <strong>A:</strong> For many low-channel or standard BCI applications, classical models provide better interpretability, require vastly less data, and run exceptionally fast during live real-time inference on edge devices.
              </p>
            </div>

            <div>
              <h4 className="font-bold text-white text-sm mb-1">Q: What exactly is real and what is simulated?</h4>
              <p className="text-sm text-neuro-muted">
                <strong>A:</strong> The 3D UI, the signal processing pipeline, the LSL integration, and the ML benchmarks are <strong>real</strong> (the benchmarks process actual PhysioNet EEG data). The live continuous LSL stream used in the default demo is <strong>simulated</strong>.
              </p>
            </div>
            
            <div className="rounded bg-neuro-bg border border-neuro-border p-4 mt-4">
              <h4 className="font-bold text-neuro-accent text-sm mb-1">Q: What would you do if given an actual OpenBCI Cyton right now?</h4>
              <p className="text-sm text-neuro-muted">
                <strong>A:</strong> 
                1. Run `make validate-openbci-cyton` to verify live stream quality.<br/>
                2. Run the physical EEG trial protocol to record a baseline eyes-open/closed session.<br/>
                3. Calculate personalization thresholds.<br/>
                4. Run live LSL shadow mode with the device to observe inference behavior safely.<br/>
                5. Only after all checks pass, manually disable the safety gate to enable closed-loop visualization.
              </p>
            </div>
          </div>
        </section>

      </div>
    </div>
  )
}
