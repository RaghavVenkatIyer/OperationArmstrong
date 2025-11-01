from flask import Flask, request, jsonify, render_template_string
import math

app = Flask(__name__)

# === Black Hole Physics Function ===
@app.route("/blackhole")
def blackhole():
    try:
        G = 6.67430e-11
        c = 3e8

        M = float(request.args.get("M", 0))
        r = float(request.args.get("r", 0))
        mode = int(request.args.get("time", 0))
        time_value = float(request.args.get("time_value", 0))
        lengthselection = request.args.get("lengthselection", "")
        viewerslength = request.args.get("viewerslength", "")
        fallerslength = request.args.get("fallerslength", "")
        m = request.args.get("m", "")
        h = request.args.get("h", "")

        if M <= 0 or r <= 0:
            return "⚠️ Invalid parameters! Mass and distance must be positive."

        rs = 2 * G * M / (c**2)
        if r <= rs:
            return "⚠️ Distance must be greater than Schwarzschild radius!"

        time_dilation = 1 / math.sqrt(1 - rs / r)

        if mode == 0:
            fallers_time = time_value / time_dilation
            viewers_time = time_value
        else:
            viewers_time = time_value * time_dilation
            fallers_time = time_value

        result = (
            f"🌀 Schwarzschild radius: {rs:.6e} m\n"
            f"⏳ Time dilation factor: {time_dilation:.6f}\n"
            f"🧍 Viewer's time: {viewers_time:.6f} s\n"
            f"🕳️ Faller's time: {fallers_time:.6f} s\n"
        )

        return result
    except Exception as e:
        return f"❌ Error: {e}"


# === HTML + JS FRONTEND ===
@app.route("/")
def index():
    html = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Black Hole Physics & Simulation (3D)</title>
<style>
body {
  font-family: 'Poppins', sans-serif;
  background: radial-gradient(circle at center, #000010, #000000);
  color: #00ffea;
  text-align: center;
  margin: 0;
  overflow: hidden;
}
.card {
  background: rgba(20, 20, 20, 0.8);
  border: 1px solid #0ff;
  border-radius: 10px;
  box-shadow: 0 0 15px #0ff4;
  padding: 15px;
  max-width: 500px;
  margin: 15px auto;
  text-align: left;
  z-index: 2;
  position: relative;
}
h1 {
  color: #0ff;
  text-shadow: 0 0 10px #0ff;
}
label { display:block; margin-top:10px; font-weight:bold; }
input {
  width: 95%;
  background: #111;
  color: #0ff;
  border: 1px solid #0ff;
  padding: 8px;
  margin-top: 5px;
  border-radius: 6px;
  font-size: 1em;
}
button {
  background: #111;
  color: #0ff;
  border: 1px solid #0ff;
  padding: 10px 20px;
  margin-top: 15px;
  border-radius: 8px;
  font-size: 1.1em;
  cursor: pointer;
  transition: 0.3s;
}
button:hover { background-color: #0ff; color: #000; }
#output {
  white-space: pre-wrap;
  background: #111;
  color: #0f0;
  padding: 15px;
  border-radius: 10px;
  border: 1px solid #0ff;
  margin-top: 20px;
  max-width: 90%;
  margin-left: auto;
  margin-right: auto;
  text-align: left;
}
#sceneContainer {
  position: fixed;
  top: 0; left: 0;
  width: 100%; height: 100%;
  z-index: 0;
  overflow: hidden;
}
</style>
</head>
<body>
<h1>🌀 Black Hole Simulation & Physics Engine</h1>

<div class="card">
  <h3>🔢 Basic Parameters</h3>
  <label>Mass of black hole (kg):</label>
  <input id="mass" type="number" step="any" placeholder="e.g. 5e30">
  <label>Distance from black hole (m):</label>
  <input id="distance" type="number" step="any" placeholder="e.g. 1e8">
  <label>Mode:</label>
  <input id="mode" type="number" placeholder="0 = viewer→faller, 1 = faller→viewer">
  <label>Time value (s):</label>
  <input id="timevalue" type="number" step="any" placeholder="e.g. 1200">
</div>

<div class="card">
  <h3>📏 Relativistic Length & Potential Parameters</h3>
  <label>Length Selection:</label>
  <input id="lengthselection" type="number" placeholder="0 = Viewer's length, 1 = Faller's length">
  <label>Viewer's Length (m):</label>
  <input id="viewerslength" type="number" step="any" placeholder="e.g. 2">
  <label>Faller's Length (m):</label>
  <input id="fallerslength" type="number" step="any" placeholder="e.g. 1.8">
  <label>Mass of object near black hole (kg):</label>
  <input id="objectmass" type="number" step="any" placeholder="e.g. 70">
  <label>Person's height (m):</label>
  <input id="height" type="number" step="any" placeholder="e.g. 1.8">
</div>

<button onclick="calculate()">🚀 Calculate & Simulate</button>

<pre id="output"></pre>
<div id="sceneContainer"></div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.getElementById('sceneContainer').appendChild(renderer.domElement);

const blackHoleGeometry = new THREE.SphereGeometry(1, 64, 64);
const blackHoleMaterial = new THREE.MeshBasicMaterial({ color: 0x000000 });
const blackHole = new THREE.Mesh(blackHoleGeometry, blackHoleMaterial);
scene.add(blackHole);

const accretionGeometry = new THREE.RingGeometry(1.2, 2, 128);
const accretionMaterial = new THREE.MeshBasicMaterial({ color: 0xff3300, side: THREE.DoubleSide });
const accretionDisk = new THREE.Mesh(accretionGeometry, accretionMaterial);
accretionDisk.rotation.x = Math.PI / 2;
scene.add(accretionDisk);

camera.position.z = 5;
function animate() {
  requestAnimationFrame(animate);
  accretionDisk.rotation.z += 0.005;
  renderer.render(scene, camera);
}
animate();

async function calculate() {
  const M = document.getElementById('mass').value;
  const r = document.getElementById('distance').value;
  const mode = document.getElementById('mode').value;
  const timevalue = document.getElementById('timevalue').value || '';
  const lengthselection = document.getElementById('lengthselection').value || '';
  const viewerslength = document.getElementById('viewerslength').value || '';
  const fallerslength = document.getElementById('fallerslength').value || '';
  const m = document.getElementById('objectmass').value || '';
  const h = document.getElementById('height').value || '';

  const url = `/blackhole?M=${M}&r=${r}&time=${mode}&time_value=${timevalue}&lengthselection=${lengthselection}&viewerslength=${viewerslength}&fallerslength=${fallerslength}&m=${m}&h=${h}`;
  
  document.getElementById('output').innerText = "⏳ Calculating...";
  try {
    const res = await fetch(url);
    const text = await res.text();
    document.getElementById('output').innerText = text;

    const rs = 2 * 6.67430e-11 * M / (3e8**2);
    const scale = Math.min(5, Math.max(0.5, rs / r * 10));
    blackHole.scale.set(scale, scale, scale);
    accretionDisk.scale.set(scale*1.5, scale*1.5, scale*1.5);
  } catch (err) {
    document.getElementById('output').innerText = "❌ Error: " + err.message;
  }
}
</script>
</body>
</html>
"""
    return render_template_string(html)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
