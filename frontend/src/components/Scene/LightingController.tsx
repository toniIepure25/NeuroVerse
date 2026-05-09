import { useFrame } from '@react-three/fiber'
import { useRef } from 'react'
import * as THREE from 'three'
import { useNeuroVerseStore } from '../../store/neuroverseStore'

const AMBIENT_MIN = 0.1
const AMBIENT_MAX = 0.8
const POINT_BASE_MIN = 0.25
const POINT_BASE_MAX = 2.4
const RIM_MIN = 0.08
const RIM_MAX = 0.85
const FROZEN_MULT = 0.18

export function LightingController() {
  const ambientRef = useRef<THREE.AmbientLight>(null)
  const pointRef = useRef<THREE.PointLight>(null)
  const rimRef = useRef<THREE.DirectionalLight>(null)
  const frozenBlend = useRef(0)
  const rimTarget = useRef(new THREE.Color())
  const env = useNeuroVerseStore((state) => state.environment)

  useFrame((_, delta) => {
    const ambient = ambientRef.current
    const point = pointRef.current
    const rim = rimRef.current
    if (!ambient || !point || !rim) return

    const li = THREE.MathUtils.clamp(env.lightIntensity, 0, 1)
    const smooth = 1 - Math.pow(0.001, delta)
    const targetFrozen = env.frozen ? 1 : 0
    frozenBlend.current = THREE.MathUtils.lerp(frozenBlend.current, targetFrozen, smooth)
    const frozenMul = THREE.MathUtils.lerp(1, FROZEN_MULT, frozenBlend.current)

    const baseAmbient = THREE.MathUtils.lerp(AMBIENT_MIN, AMBIENT_MAX, li)
    const targetAmbient = baseAmbient * frozenMul
    ambient.intensity = THREE.MathUtils.lerp(ambient.intensity, targetAmbient, smooth)

    const targetPoint = THREE.MathUtils.lerp(POINT_BASE_MIN, POINT_BASE_MAX, li) * frozenMul
    point.intensity = THREE.MathUtils.lerp(point.intensity, targetPoint, smooth)

    const targetRim = THREE.MathUtils.lerp(RIM_MIN, RIM_MAX, li) * frozenMul
    rim.intensity = THREE.MathUtils.lerp(rim.intensity, targetRim, smooth)

    const rimHue = 0.62 + env.fogDensity * 0.06 - env.objectGlow * 0.04
    rimTarget.current.setHSL(rimHue, 0.45, 0.52)
    rim.color.lerp(rimTarget.current, smooth * 0.5)
  })

  return (
    <>
      <ambientLight ref={ambientRef} color="#1a2538" intensity={0.35} />
      <pointLight
        ref={pointRef}
        position={[0, 6, 2]}
        color="#c8d4f0"
        intensity={1.2}
        distance={32}
        decay={2}
      />
      <directionalLight
        ref={rimRef}
        position={[-10, 4, -8]}
        color="#7a6cff"
        intensity={0.4}
      />
    </>
  )
}
