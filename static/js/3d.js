import * as THREE from "https://cdn.skypack.dev/three@0.129.0";
import { GLTFLoader } from "https://cdn.skypack.dev/three@0.129.0/examples/jsm/loaders/GLTFLoader.js";
import { OrbitControls } from "https://cdn.skypack.dev/three@0.129.0/examples/jsm/controls/OrbitControls.js";

// Scene setup
const scene = new THREE.Scene();

// Camera setup
const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.z = 5;

// Renderer setup
const renderer = new THREE.WebGLRenderer({ alpha: true });
renderer.setSize(window.innerWidth * 0.4, window.innerHeight * 0.4); // Adjust to fit your layout
document.getElementById("container3D").appendChild(renderer.domElement);

// Load 3D Model
const loader = new GLTFLoader();
loader.load(
  "static/3d/Gifts.glb",
  (gltf) => {
    const object = gltf.scene;
    object.scale.set(3, 3, 3);
    object.position.set(0, -1, 0); // Adjust position to center
    scene.add(object);
  },
  undefined,
  (error) => {
    console.error("Error loading the model:", error);
  }
);

// Lighting
// Hemisphere light for soft, even lighting
const hemisphereLight = new THREE.HemisphereLight(0xffffff, 0x404040, 0.8);
scene.add(hemisphereLight);

// Additional directional lights for stronger highlights
const directionalLight1 = new THREE.DirectionalLight(0xffffff, 0.6);
directionalLight1.position.set(10, 10, 10);
scene.add(directionalLight1);

const directionalLight2 = new THREE.DirectionalLight(0xffffff, 0.4);
directionalLight2.position.set(-10, -10, -10);
scene.add(directionalLight2);

// Controls
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableZoom = false;
controls.enableDamping = true;

// Animation loop
function animate() {
  requestAnimationFrame(animate);
  controls.update();
  renderer.render(scene, camera);
}

animate();

// Resize listener
window.addEventListener("resize", () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth * 0.4, window.innerHeight * 0.4);
});
