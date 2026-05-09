import { MeditationChamber } from '../Scene/MeditationChamber'
import { BiosignalPanel } from '../Dashboard/BiosignalPanel'
import { CognitiveRadar } from '../Dashboard/CognitiveRadar'
import { SafetyPanel } from '../Dashboard/SafetyPanel'
import { EventTimeline } from '../Dashboard/EventTimeline'
import { ResearchPanel } from '../Dashboard/ResearchPanel'
import { SessionControls } from '../Dashboard/SessionControls'

export function AppShell() {
  return (
    <>
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
    </>
  )
}
