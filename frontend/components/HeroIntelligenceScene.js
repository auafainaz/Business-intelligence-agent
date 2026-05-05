"use client";

import { useEffect, useRef } from "react";
import * as THREE from "three";

export default function HeroIntelligenceScene() {
  const mountRef = useRef(null);

  useEffect(() => {
    const mount = mountRef.current;
    if (!mount) {
      return undefined;
    }

    const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(42, 1, 0.1, 100);
    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true, preserveDrawingBuffer: true });
    const startedAt = performance.now();

    renderer.setClearColor(0x000000, 0);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.8));
    renderer.domElement.setAttribute("aria-hidden", "true");
    renderer.domElement.className = "h-full w-full";
    mount.appendChild(renderer.domElement);

    camera.position.set(0, 0.65, 8.6);

    const group = new THREE.Group();
    group.position.set(1.35, -0.2, 0);
    scene.add(group);

    const cyan = new THREE.Color("#77e4f2");
    const blue = new THREE.Color("#7aa7ff");
    const gold = new THREE.Color("#e7c873");

    const ringMaterial = new THREE.MeshBasicMaterial({
      color: cyan,
      transparent: true,
      opacity: 0.26,
      side: THREE.DoubleSide
    });

    const outerRing = new THREE.Mesh(new THREE.TorusGeometry(2.45, 0.012, 10, 180), ringMaterial);
    const innerRing = new THREE.Mesh(
      new THREE.TorusGeometry(1.55, 0.009, 10, 160),
      new THREE.MeshBasicMaterial({ color: blue, transparent: true, opacity: 0.2, side: THREE.DoubleSide })
    );
    const orbitRing = new THREE.Mesh(
      new THREE.TorusGeometry(3.25, 0.006, 8, 190),
      new THREE.MeshBasicMaterial({ color: gold, transparent: true, opacity: 0.16, side: THREE.DoubleSide })
    );

    outerRing.rotation.x = 1.16;
    innerRing.rotation.x = 1.16;
    innerRing.rotation.y = 0.28;
    orbitRing.rotation.x = 1.28;
    orbitRing.rotation.y = -0.34;
    group.add(outerRing, innerRing, orbitRing);

    const nodeGeometry = new THREE.SphereGeometry(0.045, 18, 18);
    const nodes = [];
    const nodePositions = [
      [-2.25, 0.46, 0.18],
      [-1.42, -1.2, 0.08],
      [-0.36, 1.42, -0.1],
      [0.68, -1.54, 0.24],
      [1.46, 0.98, -0.22],
      [2.38, -0.22, 0.04],
      [0.1, 0.06, 0.32]
    ];

    nodePositions.forEach((position, index) => {
      const material = new THREE.MeshBasicMaterial({
        color: index % 3 === 0 ? gold : cyan,
        transparent: true,
        opacity: index === nodePositions.length - 1 ? 0.9 : 0.72
      });
      const node = new THREE.Mesh(nodeGeometry, material);
      node.position.set(...position);
      nodes.push(node);
      group.add(node);
    });

    const linePositions = [
      nodePositions[0], nodePositions[2],
      nodePositions[2], nodePositions[4],
      nodePositions[4], nodePositions[5],
      nodePositions[5], nodePositions[3],
      nodePositions[3], nodePositions[1],
      nodePositions[1], nodePositions[0],
      nodePositions[6], nodePositions[0],
      nodePositions[6], nodePositions[2],
      nodePositions[6], nodePositions[4],
      nodePositions[6], nodePositions[5],
      nodePositions[6], nodePositions[3],
      nodePositions[6], nodePositions[1]
    ];
    const lineGeometry = new THREE.BufferGeometry().setFromPoints(
      linePositions.map(([x, y, z]) => new THREE.Vector3(x, y, z))
    );
    const lines = new THREE.LineSegments(
      lineGeometry,
      new THREE.LineBasicMaterial({ color: cyan, transparent: true, opacity: 0.18 })
    );
    group.add(lines);

    const panelGroup = new THREE.Group();
    panelGroup.position.set(0.6, -0.12, 0.08);
    panelGroup.rotation.y = -0.22;
    panelGroup.rotation.x = 0.06;
    group.add(panelGroup);

    const panelMaterial = new THREE.MeshBasicMaterial({
      color: 0x0f1824,
      transparent: true,
      opacity: 0.82,
      side: THREE.DoubleSide
    });
    const panel = new THREE.Mesh(new THREE.PlaneGeometry(2.1, 1.22), panelMaterial);
    panelGroup.add(panel);

    const accentBars = [
      [-0.56, 0.3, 0.72, cyan],
      [-0.38, 0.02, 1.12, blue],
      [-0.72, -0.26, 0.48, gold],
      [0.52, -0.26, 0.42, cyan]
    ];
    accentBars.forEach(([x, y, width, color]) => {
      const bar = new THREE.Mesh(
        new THREE.PlaneGeometry(width, 0.045),
        new THREE.MeshBasicMaterial({ color, transparent: true, opacity: 0.72, side: THREE.DoubleSide })
      );
      bar.position.set(x, y, 0.015);
      panelGroup.add(bar);
    });

    const particleCount = 220;
    const particlePositions = new Float32Array(particleCount * 3);
    for (let index = 0; index < particleCount; index += 1) {
      particlePositions[index * 3] = (Math.random() - 0.5) * 11;
      particlePositions[index * 3 + 1] = (Math.random() - 0.5) * 6;
      particlePositions[index * 3 + 2] = (Math.random() - 0.5) * 4 - 0.8;
    }
    const particleGeometry = new THREE.BufferGeometry();
    particleGeometry.setAttribute("position", new THREE.BufferAttribute(particlePositions, 3));
    const particles = new THREE.Points(
      particleGeometry,
      new THREE.PointsMaterial({
        color: 0x77e4f2,
        size: 0.018,
        transparent: true,
        opacity: 0.42,
        depthWrite: false
      })
    );
    scene.add(particles);

    const resize = () => {
      const { width, height } = mount.getBoundingClientRect();
      renderer.setSize(width, height, false);
      camera.aspect = width / Math.max(height, 1);
      camera.updateProjectionMatrix();
      group.scale.setScalar(width < 760 ? 0.68 : 1);
      group.position.x = width < 760 ? 0.2 : 1.35;
      group.position.y = width < 760 ? -0.68 : -0.2;
    };

    resize();
    const resizeObserver = new ResizeObserver(resize);
    resizeObserver.observe(mount);

    let frameId = 0;
    const render = () => {
      const elapsed = (performance.now() - startedAt) / 1000;
      const speed = prefersReducedMotion ? 0.08 : 1;

      group.rotation.y = Math.sin(elapsed * 0.18 * speed) * 0.12;
      outerRing.rotation.z = elapsed * 0.12 * speed;
      innerRing.rotation.z = -elapsed * 0.17 * speed;
      orbitRing.rotation.z = elapsed * 0.08 * speed;
      particles.rotation.y = elapsed * 0.025 * speed;

      nodes.forEach((node, index) => {
        const pulse = 1 + Math.sin(elapsed * 1.7 * speed + index) * 0.18;
        node.scale.setScalar(pulse);
      });

      panelGroup.position.y = -0.12 + Math.sin(elapsed * 0.9 * speed) * 0.055;
      renderer.render(scene, camera);
      frameId = window.requestAnimationFrame(render);
    };
    render();

    return () => {
      window.cancelAnimationFrame(frameId);
      resizeObserver.disconnect();
      mount.removeChild(renderer.domElement);
      scene.traverse((object) => {
        if (object.geometry) {
          object.geometry.dispose();
        }
        if (object.material) {
          if (Array.isArray(object.material)) {
            object.material.forEach((material) => material.dispose());
          } else {
            object.material.dispose();
          }
        }
      });
      renderer.dispose();
    };
  }, []);

  return (
    <div
      ref={mountRef}
      className="pointer-events-none absolute inset-x-0 top-0 z-0 h-screen min-h-[720px] overflow-hidden opacity-95"
    />
  );
}
