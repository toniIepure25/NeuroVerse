import { MeditationChamber } from '../Scene/MeditationChamber'
import { BiosignalPanel } from '../Dashboard/BiosignalPanel'
import { CognitiveRadar } from '../Dashboard/CognitiveRadar'
import { SafetyPanel } from '../Dashboard/SafetyPanel'
import { EventTimeline } from '../Dashboard/EventTimeline'
import { ResearchPanel } from '../Dashboard/ResearchPanel'
import { SessionControls } from '../Dashboard/SessionControls'

export function AppShell() {
  return (
    <div className="flex h-screen w-screen flex-col overflow-hidden bg-neuro-bg text-neuro-text">
      <header className="flex shrink-0 items-center justify-between border-b border-neuro-border px-6 py-3">
        <div className="flex items-center gap-3">
          <div className="h-3 w-3 rounded-full bg-neuro-accent" />
          <h1 className="text-lg font-semibold tracking-tight">NeuroVerse</h1>
        </div>
        <span className="text-xs text-neuro-muted">Neuroadaptive Interface Platform</span>
      </header>

      <div className="flex min-h-0 flex-1">
        <main className="relative flex-[3] border-r border-neuro-border">
          <MeditationChamber />
        </main>

        <aside className="flex w-[420px] shrink-0 flex-col gap-3 overflow-y-auto p-4">
          <SessionControls />
          <CognitiveRadar />
          <BiosignalPanel />
          <SafetyPanel />
          <ResearchPanel />
          <EventTimeline />
        </aside>
      </div>
    </div>
  )
}
