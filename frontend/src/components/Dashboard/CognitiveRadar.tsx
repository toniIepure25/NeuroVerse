import {
  PolarAngleAxis,
  PolarGrid,
  PolarRadiusAxis,
  Radar,
  RadarChart,
  ResponsiveContainer,
} from 'recharts'
import { useNeuroVerseStore } from '../../store/neuroverseStore'

const DIMENSIONS = [
  { key: 'focus' as const, label: 'Focus' },
  { key: 'relaxation' as const, label: 'Relaxation' },
  { key: 'workload' as const, label: 'Workload' },
  { key: 'stress' as const, label: 'Stress' },
  { key: 'fatigue' as const, label: 'Fatigue' },
  { key: 'imagery_engagement' as const, label: 'Imagery' },
] as const

export function CognitiveRadar() {
  const cognitiveState = useNeuroVerseStore((state) => state.cognitiveState)

  if (!cognitiveState) {
    return (
      <div className="flex h-[280px] items-center justify-center rounded-lg border border-neuro-border bg-neuro-surface px-4">
        <p className="text-sm text-neuro-muted">Awaiting data...</p>
      </div>
    )
  }

  const chartData = DIMENSIONS.map(({ key, label }) => ({
    dimension: label,
    value: Math.round(Math.min(100, Math.max(0, cognitiveState[key] * 100))),
  }))

  const confidencePct = Math.round(
    Math.min(100, Math.max(0, cognitiveState.confidence * 100))
  )

  return (
    <div className="rounded-lg border border-neuro-border bg-neuro-surface p-4 font-sans">
      <div className="mb-3 border-b border-neuro-border pb-3">
        <h3 className="text-sm font-medium tracking-tight text-neuro-text">
          Cognitive state
        </h3>
        <p className="mt-1 text-xs text-neuro-muted">
          Confidence{' '}
          <span className="tabular-nums text-neuro-accent">{confidencePct}%</span>
          <span className="text-neuro-muted"> · scale 0–100%</span>
        </p>
      </div>
      <div className="h-[240px] w-full">
        <ResponsiveContainer width="100%" height="100%">
          <RadarChart cx="50%" cy="52%" outerRadius="72%" data={chartData}>
            <PolarGrid stroke="#312e81" strokeDasharray="3 3" opacity={0.85} />
            <PolarAngleAxis
              dataKey="dimension"
              tick={{
                fill: '#94a3b8',
                fontSize: 11,
                fontFamily: 'system-ui, sans-serif',
              }}
            />
            <PolarRadiusAxis
              angle={90}
              domain={[0, 100]}
              tick={{ fill: '#64748b', fontSize: 10 }}
              tickCount={5}
            />
            <Radar
              name="Score"
              dataKey="value"
              stroke="#a78bfa"
              strokeWidth={2}
              fill="#6366f1"
              fillOpacity={0.45}
            />
          </RadarChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
