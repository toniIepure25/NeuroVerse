import { Canvas, useFrame } from '@react-three/fiber'
import { useRef } from 'react'
import * as THREE from 'three'
import { useNeuroVerseStore } from '../../store/neuroverseStore'
import { AdaptiveEnvironment } from './AdaptiveEnvironment'
import { LightingController } from './LightingController'
import { Particles } from './Particles'

const FOG_COLOR = '#0a0e1a'
/** Initial fog args — near/far lerp toward heavy fog (2, 8) as fogDensity → 1 */
const FOG_ARGS_CLEAR: [number, number] = [15, 50]
const [NEAR_CLEAR, FAR_CLEAR] = FOG_ARGS_CLEAR
const NEAR_HEAVY = 2
const FAR_HEAVY = 8

function FogLerp() {
  const fogRef = useRef<THREE.Fog>(null)
  const fogDensity = useNeuroVerseStore((state) => state.environment.fogDensity)

  useFrame((_, delta) => {
    const fog = fogRef.current
    if (!fog) return
    const t = THREE.MathUtils.clamp(fogDensity, 0, 1)
    const targetNear = THREE.MathUtils.lerp(NEAR_CLEAR, NEAR_HEAVY, t)
    const targetFar = THREE.MathUtils.lerp(FAR_CLEAR, FAR_HEAVY, t)
    const smooth = 1 - Math.pow(0.001, delta)
    fog.near = THREE.MathUtils.lerp(fog.near, targetNear, smooth)
    fog.far = THREE.MathUtils.lerp(fog.far, targetFar, smooth)
  })

  return <fog ref={fogRef} attach="fog" args={[FOG_COLOR, ...FOG_ARGS_CLEAR]} />
}

export function MeditationChamber() {
  return (
    <div className="w-full h-full">
      <Canvas camera={{ position: [0, 2, 8], fov: 60 }} gl={{ antialias: true, alpha: false }}>
        <color attach="background" args={[FOG_COLOR]} />
        <FogLerp />
        <AdaptiveEnvironment />
        <Particles />
        <LightingController />
      </Canvas>
    </div>
  )
}
