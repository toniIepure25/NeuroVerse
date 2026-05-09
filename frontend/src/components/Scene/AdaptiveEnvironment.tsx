import { useFrame } from '@react-three/fiber'
import { Float, MeshDistortMaterial } from '@react-three/drei'
import { type ReactNode, useMemo, useRef } from 'react'
import * as THREE from 'three'
import { useNeuroVerseStore } from '../../store/neuroverseStore'

const GROUND_Y = -1

type FloatMeshProps = {
  children: ReactNode
  position: [number, number, number]
  rotationSpeed: [number, number, number]
  motionScale: number
  frozen: boolean
}

function FloatingShape({ children, position, rotationSpeed, motionScale, frozen }: FloatMeshProps) {
  const ref = useRef<THREE.Group>(null)
  const smoothedMotion = useRef(0)

  useFrame((_, delta) => {
    const group = ref.current
    if (!group) return
    const targetMotion = frozen ? 0 : motionScale
    smoothedMotion.current = THREE.MathUtils.lerp(smoothedMotion.current, targetMotion, 1 - Math.pow(0.001, delta))
    const m = smoothedMotion.current
    group.rotation.x += rotationSpeed[0] * delta * m
    group.rotation.y += rotationSpeed[1] * delta * m
    group.rotation.z += rotationSpeed[2] * delta * m
  })

  const drift = frozen ? 0 : 1.2 * motionScale

  return (
    <Float speed={drift} rotationIntensity={0.25 * (frozen ? 0 : motionScale)} floatIntensity={0.4 * (frozen ? 0 : motionScale)}>
      <group ref={ref} position={position}>
        {children}
      </group>
    </Float>
  )
}

const shapeConfigs: Array<{
  position: [number, number, number]
  rotationSpeed: [number, number, number]
  kind: 'icosa' | 'torus' | 'octa'
}> = [
  { position: [-2.8, 1.2, -1.5], rotationSpeed: [0.08, 0.12, 0.04], kind: 'icosa' },
  { position: [3.2, 0.6, -0.8], rotationSpeed: [0.05, 0.1, 0.07], kind: 'torus' },
  { position: [-1.2, 2.4, 1.2], rotationSpeed: [0.06, 0.05, 0.09], kind: 'octa' },
  { position: [2.4, 2.0, 2.0], rotationSpeed: [0.07, 0.08, 0.05], kind: 'icosa' },
  { position: [-3.0, -0.2, 2.5], rotationSpeed: [0.04, 0.11, 0.06], kind: 'octa' },
  { position: [1.0, 1.8, -2.8], rotationSpeed: [0.09, 0.04, 0.08], kind: 'torus' },
]

function CentralSymbol() {
  const meshRef = useRef<THREE.Mesh>(null)
  const materialRef = useRef<THREE.MeshStandardMaterial>(null)
  const env = useNeuroVerseStore((state) => state.environment)
  const smoothedGlow = useRef(0)
  const smoothedMotion = useRef(0)

  const tmpEmissive = useMemo(() => new THREE.Color(), [])
  const tmpFogTint = useMemo(() => new THREE.Color('#7ee8ff'), [])

  useFrame((_, delta) => {
    const mesh = meshRef.current
    const mat = materialRef.current
    if (!mesh || !mat) return
    const smooth = 1 - Math.pow(0.001, delta)
    const targetGlow = THREE.MathUtils.clamp(env.objectGlow, 0, 1)
    smoothedGlow.current = THREE.MathUtils.lerp(smoothedGlow.current, targetGlow, smooth)

    const g = smoothedGlow.current
    mesh.visible = g > 0.02
    const targetMotion = env.frozen ? 0 : env.motionSpeed
    smoothedMotion.current = THREE.MathUtils.lerp(smoothedMotion.current, targetMotion, smooth)
    const m = smoothedMotion.current
    mesh.rotation.y += 0.35 * delta * m
    mesh.rotation.x += 0.12 * delta * m

    tmpEmissive.set('#6b5cff').lerp(tmpFogTint, env.fogDensity * 0.4)
    mat.emissive.copy(tmpEmissive)
    mat.emissiveIntensity = THREE.MathUtils.lerp(0, 2.2, g)
    mat.opacity = Math.min(1, g * 1.1)
    mat.transparent = g < 0.99
  })

  return (
    <mesh ref={meshRef} position={[0, 0.9, 0]}>
      <dodecahedronGeometry args={[0.85, 0]} />
      <meshStandardMaterial
        ref={materialRef}
        color="#1a1530"
        metalness={0.75}
        roughness={0.22}
        emissive="#000000"
        emissiveIntensity={0}
        transparent
      />
    </mesh>
  )
}

export function AdaptiveEnvironment() {
  const env = useNeuroVerseStore((state) => state.environment)
  const groundMat = useMemo(
    () =>
      new THREE.MeshStandardMaterial({
        color: '#04060c',
        metalness: 0.92,
        roughness: 0.38,
        envMapIntensity: 0.35,
      }),
    [],
  )

  return (
    <group>
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, GROUND_Y, 0]} material={groundMat}>
        <circleGeometry args={[14, 72]} />
      </mesh>

      <CentralSymbol />

      {shapeConfigs.map((cfg, i) => (
        <FloatingShape
          key={i}
          position={cfg.position}
          rotationSpeed={cfg.rotationSpeed}
          motionScale={env.motionSpeed}
          frozen={env.frozen}
        >
          {cfg.kind === 'icosa' && (
            <mesh castShadow receiveShadow>
              <icosahedronGeometry args={[0.45, 0]} />
              <meshStandardMaterial color="#12182a" metalness={0.7} roughness={0.35} />
            </mesh>
          )}
          {cfg.kind === 'torus' && (
            <mesh castShadow receiveShadow>
              <torusGeometry args={[0.38, 0.12, 16, 48]} />
              <MeshDistortMaterial
                color="#0f1424"
                metalness={0.65}
                roughness={0.4}
                distort={0.12}
                speed={env.frozen ? 0 : 1.2 * env.motionSpeed}
              />
            </mesh>
          )}
          {cfg.kind === 'octa' && (
            <mesh castShadow receiveShadow>
              <octahedronGeometry args={[0.42, 0]} />
              <meshStandardMaterial color="#101a2e" metalness={0.75} roughness={0.32} />
            </mesh>
          )}
        </FloatingShape>
      ))}
    </group>
  )
}
