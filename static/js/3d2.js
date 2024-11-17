import * as THREE from "https://cdn.skypack.dev/three@0.129.0";
import { GLTFLoader } from "https://cdn.skypack.dev/three@0.129.0/examples/jsm/loaders/GLTFLoader.js";
import { OrbitControls } from "https://cdn.skypack.dev/three@0.129.0/examples/jsm/controls/OrbitControls.js";
// Common Imports
const loader = new GLTFLoader();

// ----------------------------
// Scene, Camera, Renderer for Logo
// ----------------------------
const sceneLogo = new THREE.Scene();
const cameraLogo = new THREE.PerspectiveCamera(10, window.innerWidth / window.innerHeight, 0.1, 1000);
cameraLogo.position.z = 15;

const rendererLogo = new THREE.WebGLRenderer({ alpha: true });
rendererLogo.setSize(window.innerWidth * 0.5, window.innerHeight * 0.5);
document.getElementById("hero-image").appendChild(rendererLogo.domElement);

// Load Logo Model
loader.load(
  "static/3d/logo.gltf",
  (gltf) => {
    const logoObject = gltf.scene;
    logoObject.scale.set(0.001, 0.001, 0.001); // Adjust size of the logo
    logoObject.position.set(0, 0, 0); // Adjust position to center
    sceneLogo.add(logoObject);
  },
  undefined,
  (error) => {
    console.error("Error loading the logo model:", error);
  }
);

const hemisphereLight = new THREE.HemisphereLight(0xffffff, 0x404040, 0.8);
sceneLogo.add(hemisphereLight);

// Additional directional lights for stronger highlights
const directionalLight1 = new THREE.DirectionalLight(0xffffff, 0.6);
directionalLight1.position.set(10, 10, 10);
sceneLogo.add(directionalLight1);

const directionalLight2 = new THREE.DirectionalLight(0xffffff, 0.4);
directionalLight2.position.set(-10, -10, -10);
sceneLogo.add(directionalLight2);

// Controls for Logo
const controlsLogo = new OrbitControls(cameraLogo, rendererLogo.domElement);
controlsLogo.enableZoom = false;
controlsLogo.enableDamping = true;

// Animation Loop for Logo
function animateLogo() {
  requestAnimationFrame(animateLogo);
  controlsLogo.update();
  rendererLogo.render(sceneLogo, cameraLogo);
}
animateLogo();

// ----------------------------
// Scene, Camera, Renderer for T-Shirt
// ----------------------------
const sceneTshirt = new THREE.Scene();
const cameraTshirt = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
cameraTshirt.position.z = 5;

const rendererTshirt = new THREE.WebGLRenderer({ alpha: true });
rendererTshirt.setSize(window.innerWidth * 0.5, window.innerHeight * 0.5);
document.getElementById("featured-image").appendChild(rendererTshirt.domElement);

// Load T-Shirt Model
loader.load(
  "static/3d/tshirt/scene.gltf",
  (gltf) => {
    const tshirtObject = gltf.scene;
    tshirtObject.scale.set(2.5, 2.5, 2.5); // Adjust size of the T-shirt
    tshirtObject.position.set(0, -0.5, 0); // Adjust position to center
    sceneTshirt.add(tshirtObject);
  },
  undefined,
  (error) => {
    console.error("Error loading the T-shirt model:", error);
  }
);

// Lighting for T-Shirt
const lightTshirt = new THREE.DirectionalLight(0xffffff, 1);
lightTshirt.position.set(10, 10, 10);
sceneTshirt.add(lightTshirt);

const ambientLightTshirt = new THREE.AmbientLight(0x404040);
sceneTshirt.add(ambientLightTshirt);

// Controls for T-Shirt
const controlsTshirt = new OrbitControls(cameraTshirt, rendererTshirt.domElement);
controlsTshirt.enableZoom = false;
controlsTshirt.enableDamping = true;

// Animation Loop for T-Shirt
function animateTshirt() {
  requestAnimationFrame(animateTshirt);
  controlsTshirt.update();
  rendererTshirt.render(sceneTshirt, cameraTshirt);
}
animateTshirt();

// ----------------------------
// Handle Window Resizing
// ----------------------------
window.addEventListener("resize", () => {
  // Update Logo
  cameraLogo.aspect = window.innerWidth / window.innerHeight;
  cameraLogo.updateProjectionMatrix();
  rendererLogo.setSize(window.innerWidth * 0.5, window.innerHeight * 0.5);

  // Update T-Shirt
  cameraTshirt.aspect = window.innerWidth / window.innerHeight;
  cameraTshirt.updateProjectionMatrix();
  rendererTshirt.setSize(window.innerWidth * 0.5, window.innerHeight * 0.5);
});
