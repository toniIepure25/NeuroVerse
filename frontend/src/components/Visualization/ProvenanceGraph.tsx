import React from 'react'

export interface ProvenanceNode {
  id: string
  label: string
  status: 'valid' | 'warning' | 'missing' | 'blocked' | 'static'
  source: 'external_imagina' | 'neuroverse_runtime' | 'static_snapshot' | 'fixture_fallback'
  path?: string
  description: string
}

interface ProvenanceGraphProps {
  nodes: ProvenanceNode[]
}

export const ProvenanceGraph: React.FC<ProvenanceGraphProps> = ({ nodes }) => {
  const getStatusColor = (status: ProvenanceNode['status']) => {
    switch (status) {
      case 'valid':
        return 'border-emerald-500/50 bg-emerald-950/20 text-emerald-400'
      case 'warning':
        return 'border-amber-500/50 bg-amber-950/20 text-amber-400'
      case 'blocked':
        return 'border-rose-500/50 bg-rose-950/20 text-rose-400'
      case 'static':
        return 'border-sky-500/50 bg-sky-950/20 text-sky-400'
      case 'missing':
      default:
        return 'border-zinc-700 bg-zinc-900/50 text-zinc-500'
    }
  }

  const getStatusIcon = (status: ProvenanceNode['status']) => {
    switch (status) {
      case 'valid':
        return (
          <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
          </svg>
        )
      case 'warning':
        return (
          <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        )
      case 'blocked':
        return (
          <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
          </svg>
        )
      case 'static':
        return (
          <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7v12m0 0l-4-4m4 4l4-4m0 6V7m0 0l-4 4m4-4l4 4" />
          </svg>
        )
      case 'missing':
      default:
        return (
          <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636" />
          </svg>
        )
    }
  }

  const getSourceLabel = (source: ProvenanceNode['source']) => {
    switch (source) {
      case 'external_imagina':
        return 'External IMAGINA'
      case 'neuroverse_runtime':
        return 'NeuroVerse Runtime'
      case 'static_snapshot':
        return 'Static Snapshot'
      case 'fixture_fallback':
        return 'Fixture Fallback'
      default:
        return 'Unknown'
    }
  }

  return (
    <div className="relative w-full overflow-x-auto rounded-xl border border-neuro-border bg-neuro-surface/30 p-6 backdrop-blur-md">
      <div className="mb-4 flex items-center justify-between">
        <div>
          <h3 className="text-sm font-semibold tracking-wide text-neuro-text uppercase">Data & Decision Provenance Flow</h3>
          <p className="text-xs text-neuro-muted">How model inferences and EEG validation maps to the final safe corridor interface.</p>
        </div>
        <div className="flex flex-wrap gap-2 text-[10px]">
          <span className="flex items-center gap-1 rounded bg-emerald-950/40 px-2 py-0.5 border border-emerald-500/20 text-emerald-400">
            <span className="h-1.5 w-1.5 rounded-full bg-emerald-400" /> Active/Valid
          </span>
          <span className="flex items-center gap-1 rounded bg-sky-950/40 px-2 py-0.5 border border-sky-500/20 text-sky-400">
            <span className="h-1.5 w-1.5 rounded-full bg-sky-400" /> Static Snapshots
          </span>
          <span className="flex items-center gap-1 rounded bg-rose-950/40 px-2 py-0.5 border border-rose-500/20 text-rose-400">
            <span className="h-1.5 w-1.5 rounded-full bg-rose-400" /> Locked/Blocked
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-5 gap-y-8 gap-x-4 min-w-[800px] relative py-4">
        {/* Row 1: External Research Boundary */}
        <div className="flex flex-col gap-6">
          <div className="text-center text-[10px] font-bold tracking-widest text-neuro-muted uppercase border-b border-neuro-border pb-1">
            1. Research Model
          </div>
          {nodes.filter(n => ['external_imagina_export', 'neuroverse_export_validator'].includes(n.id)).map((node, i) => (
            <div key={node.id} className="relative">
              {renderNodeCard(node)}
              {i === 0 && renderRightArrow()}
            </div>
          ))}
        </div>

        {/* Row 2: Import & Fusion */}
        <div className="flex flex-col gap-6">
          <div className="text-center text-[10px] font-bold tracking-widest text-neuro-muted uppercase border-b border-neuro-border pb-1">
            2. Import & Fusion
          </div>
          {nodes.filter(n => ['import_summary', 'fusion_packet'].includes(n.id)).map((node, i) => (
            <div key={node.id} className="relative">
              {renderNodeCard(node)}
              {renderRightArrow()}
            </div>
          ))}
        </div>

        {/* Row 3: Safety Enforcement */}
        <div className="flex flex-col gap-6">
          <div className="text-center text-[10px] font-bold tracking-widest text-neuro-muted uppercase border-b border-neuro-border pb-1">
            3. Safety Governance
          </div>
          {nodes.filter(n => ['safety_governance'].includes(n.id)).map(node => (
            <div key={node.id} className="relative">
              {renderNodeCard(node)}
              {renderRightArrow()}
            </div>
          ))}
        </div>

        {/* Row 4: Protocol Runtime */}
        <div className="flex flex-col gap-6">
          <div className="text-center text-[10px] font-bold tracking-widest text-neuro-muted uppercase border-b border-neuro-border pb-1">
            4. Protocol Execution
          </div>
          {nodes.filter(n => ['protocol_run', 'completion_report'].includes(n.id)).map((node, i) => (
            <div key={node.id} className="relative">
              {renderNodeCard(node)}
              {renderRightArrow()}
            </div>
          ))}
        </div>

        {/* Row 5: Evidence Pack & UI Scaffold */}
        <div className="flex flex-col gap-6">
          <div className="text-center text-[10px] font-bold tracking-widest text-neuro-muted uppercase border-b border-neuro-border pb-1">
            5. UI & Audit Artifacts
          </div>
          {nodes.filter(n => ['evidence_pack', 'static_portfolio_snapshot', 'dream_corridor_shadow_mapping'].includes(n.id)).map(node => (
            <div key={node.id} className="relative">
              {renderNodeCard(node)}
            </div>
          ))}
        </div>
      </div>

      <div className="mt-4 rounded-lg bg-neuro-surface/20 border border-neuro-border p-3 text-xs text-neuro-muted">
        <p className="flex items-center gap-2">
          <span className="h-2 w-2 rounded-full bg-rose-500 animate-pulse" />
          <span className="font-semibold text-neuro-text">Safety Boundary Isolation:</span>
          IMAGINA model output is never wired directly to real-time physical closed-loop adaptation. All adaptation pathways remain strictly in <span className="text-neuro-accent font-semibold">shadow-only mode</span> and subject to multi-layered safety gates.
        </p>
      </div>
    </div>
  )

  function renderNodeCard(node: ProvenanceNode) {
    return (
      <div className={`flex flex-col rounded-lg border p-3 transition-all hover:scale-[1.02] hover:shadow-[0_0_12px_rgba(45,212,191,0.1)] ${getStatusColor(node.status)}`}>
        <div className="flex items-start justify-between gap-2">
          <span className="text-xs font-semibold tracking-tight text-neuro-text">{node.label}</span>
          <span className="shrink-0">{getStatusIcon(node.status)}</span>
        </div>
        <p className="mt-1 text-[10px] leading-relaxed text-neuro-muted">{node.description}</p>
        <div className="mt-2 flex items-center justify-between text-[9px]">
          <span className="rounded bg-neuro-surface/40 px-1 py-0.5 border border-neuro-border text-neuro-muted">
            {getSourceLabel(node.source)}
          </span>
          <span className="font-mono text-neuro-accent uppercase tracking-wider text-[8px]">
            {node.status}
          </span>
        </div>
        {node.path && (
          <div className="mt-1.5 border-t border-neuro-border/20 pt-1 font-mono text-[8px] text-neuro-muted truncate hover:text-neuro-accent transition cursor-pointer" title={node.path}>
            📂 {node.path.split('/').pop()}
          </div>
        )}
      </div>
    )
  }

  function renderRightArrow() {
    return (
      <div className="absolute top-1/2 -right-4 -translate-y-1/2 hidden md:flex items-center justify-center text-neuro-muted z-10">
        <svg className="h-4 w-4 text-neuro-accent/40 animate-pulse" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
        </svg>
      </div>
    )
  }
}
