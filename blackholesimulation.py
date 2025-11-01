from flask import Flask, request, jsonify
from flask_cors import CORS
import math

app = Flask(__name__)
CORS(app)

# Constants
G = 6.67430e-11  # gravitational constant
c = 299792458    # speed of light in m/s

@app.route("/blackhole", methods=["GET"])
def blackhole():
    try:
        # Get parameters from query string
        M = float(request.args.get("M", 0))   # Black hole mass
        r = float(request.args.get("r", 0))   # Distance from black hole
        t = float(request.args.get("t", 0))   # Input time (either faller/viewer)

        if M <= 0 or r <= 0:
            return jsonify({"error": "Mass and distance must be positive values."}), 400

        # Schwarzschild radius
        Rs = 2 * G * M / c**2

        if r <= Rs:
            return jsonify({"error": "Distance must be greater than Schwarzschild radius."}), 400

        # Time dilation factor
        dilation_factor = 1 / math.sqrt(1 - Rs / r)

        # Derived times
        faller_time = t / dilation_factor
        viewer_time = t * dilation_factor

        # Gravitational potential curvature (approx)
        curvature = G * M / (r**3)

        result = {
            "mass": M,
            "distance": r,
            "Rs": Rs,
            "time_dilation_factor": dilation_factor,
            "faller_time": faller_time,
            "viewer_time": viewer_time,
            "curvature": curvature
        }

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
