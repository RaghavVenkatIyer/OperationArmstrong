import math
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Constants
G = 6.674e-11
c = 3.0e8

@app.route('/')
def home():
    # Serve the full interactive simulation frontend
    return render_template_string(open("templates/index.html", "r").read())

@app.route('/blackhole')
def blackhole():
    try:
        # Parse inputs
        M = float(request.args.get('M', 0))
        r = float(request.args.get('r', 0))
        mode = str(request.args.get('mode', '0'))
        t_value = float(request.args.get('time', 0)) if request.args.get('time') else None
        lengthselection = request.args.get('lengthselection', None)
        viewerslength = request.args.get('viewerslength', None)
        fallerslength = request.args.get('fallerslength', None)
        m = float(request.args.get('m', 0)) if request.args.get('m') else None
        h = float(request.args.get('h', 0)) if request.args.get('h') else None

        if M <= 0 or r <= 0:
            return jsonify({"error": "Mass (M) and distance (r) must be positive."}), 400

        # Compute Schwarzschild radius
        r_s = (2 * G * M) / c**2
        if r <= r_s:
            return jsonify({"error": "Distance (r) must be greater than Schwarzschild radius."}), 400

        results = {
            "Schwarzschild_radius": r_s,
            "Escape_velocity": math.sqrt((2 * G * M) / r),
            "Gravitational_acceleration": (G * M) / r**2,
            "Orbital_velocity": math.sqrt((G * M) / r),
            "Gravitational_redshift": (1 / math.sqrt(1 - (r_s / r))) - 1,
        }

        # Time dilation calculations
        if t_value:
            if mode == '0':  # viewer → faller
                t_faller = t_value * math.sqrt(1 - r_s / r)
                results["Faller_time"] = t_faller
            else:  # faller → viewer
                t_viewer = t_value / math.sqrt(1 - r_s / r)
                results["Viewer_time"] = t_viewer

        # Length contraction
        if lengthselection is not None:
            try:
                ls = int(lengthselection)
                if ls == 0 and viewerslength:
                    viewers_len = float(viewerslength)
                    faller_len = viewers_len * math.sqrt(1 - r_s / r)
                    results["Faller_length"] = faller_len
                elif ls == 1 and fallerslength:
                    faller_len = float(fallerslength)
                    viewers_len = faller_len / math.sqrt(1 - r_s / r)
                    results["Viewer_length"] = viewers_len
            except ValueError:
                pass

        # Potential energy and tidal forces
        if m:
            results["Gravitational_potential_energy"] = -((G * m * M) / r)
        if h:
            results["Tidal_force"] = (2 * G * M * h) / (r ** 3)

        # Hover acceleration & orbital period
        results["Hover_acceleration"] = (G * M / r ** 2) * math.sqrt(1 - (r_s / r))
        results["Orbital_period"] = 2 * math.pi * math.sqrt(r ** 3 / (G * M))

        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
