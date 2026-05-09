import { useFrame } from '@react-three/fiber'
import { useEffect, useMemo, useRef } from 'react'
import * as THREE from 'three'
import { useNeuroVerseStore } from '../../store/neuroverseStore'

const MAX_PARTICLES = 200
const BOUNDS = { x: 9, yMin: -0.8, yMax: 7 }
const BASE_DRIFT = 0.35

export function Particles() {
  const pointsRef = useRef<
    THREE.Points<THREE.BufferGeometry, THREE.PointsMaterial>
  >(null)
  const env = useNeuroVerseStore((state) => state.environment)
  const velocitiesRef = useRef<Float32Array | null>(null)
  const smoothedCount = useRef(env.particleCount)
  const smoothedSpeed = useRef(env.motionSpeed)
  const colorScratch = useRef({
    base: new THREE.Color(),
    accent: new THREE.Color(),
    deep: new THREE.Color(),
    target: new THREE.Color(),
  })

  const geometry = useMemo(() => {
    const geo = new THREE.BufferGeometry()
    const positions = new Float32Array(MAX_PARTICLES * 3)
    const vels = new Float32Array(MAX_PARTICLES)
    const rnd = (a: number, b: number) => a + Math.random() * (b - a)
    for (let i = 0; i < MAX_PARTICLES; i++) {
      positions[i * 3] = rnd(-BOUNDS.x, BOUNDS.x)
      positions[i * 3 + 1] = rnd(BOUNDS.yMin, BOUNDS.yMax)
      positions[i * 3 + 2] = rnd(-6, 6)
      vels[i] = rnd(0.4, 1.2)
    }
    velocitiesRef.current = vels
    geo.setAttribute('position', new THREE.BufferAttribute(positions, 3))
    geo.setDrawRange(0, MAX_PARTICLES)
    return geo
  }, [])

  useEffect(() => {
    return () => {
      geometry.dispose()
    }
  }, [geometry])

  useFrame((_, delta) => {
    const points = pointsRef.current
    const geom = points?.geometry
    const posAttr = geom?.getAttribute('position') as THREE.BufferAttribute | undefined
    const vels = velocitiesRef.current
    if (!points || !geom || !posAttr || !vels) return

    const targetCount = THREE.MathUtils.clamp(env.particleCount, 20, MAX_PARTICLES)
    smoothedCount.current = THREE.MathUtils.lerp(
      smoothedCount.current,
      targetCount,
      1 - Math.pow(0.001, delta),
    )
    const drawCount = Math.round(
      THREE.MathUtils.clamp(smoothedCount.current, 20, MAX_PARTICLES),
    )
    geom.setDrawRange(0, drawCount)

    const targetFrozen = env.frozen ? 0 : env.motionSpeed
    smoothedSpeed.current = THREE.MathUtils.lerp(smoothedSpeed.current, targetFrozen, 1 - Math.pow(0.001, delta))
    const speedMul = smoothedSpeed.current

    const arr = posAttr.array as Float32Array
    const rise = BASE_DRIFT * speedMul * delta

    for (let i = 0; i < drawCount; i++) {
      const iy = i * 3 + 1
      if (speedMul < 0.001) continue
      arr[iy] += vels[i] * rise
      if (arr[iy] > BOUNDS.yMax) {
        arr[iy] = BOUNDS.yMin + Math.random() * 0.5
        arr[i * 3] = (Math.random() - 0.5) * 2 * BOUNDS.x
        arr[i * 3 + 2] = (Math.random() - 0.5) * 12
      }
    }
    posAttr.needsUpdate = true

    const mat = points.material as THREE.PointsMaterial
    const { base, accent, deep, target } = colorScratch.current
    const chill = 1 - env.fogDensity * 0.35
    const glow = env.objectGlow
    base.set('#4a6288').multiplyScalar(0.35 + env.lightIntensity * 0.45)
    accent.set('#8b7cff').multiplyScalar(0.15 + glow * 0.55)
    deep.set('#1c2838').multiplyScalar(env.lightIntensity * 0.25)
    target.copy(base).lerp(accent, glow * 0.5 + env.fogDensity * 0.15).lerp(deep, 0.25)
    target.multiplyScalar(chill)
    mat.color.lerp(target, 1 - Math.pow(0.001, delta))
    mat.opacity = THREE.MathUtils.lerp(mat.opacity, 0.45 + env.lightIntensity * 0.35, 1 - Math.pow(0.001, delta))
  })

  return (
    <points ref={pointsRef} geometry={geometry} frustumCulled={false}>
      <pointsMaterial
        size={0.06}
        transparent
        opacity={0.65}
        depthWrite={false}
        blending={THREE.AdditiveBlending}
        sizeAttenuation
        color="#5a6d8f"
      />
    </points>
  )
}
