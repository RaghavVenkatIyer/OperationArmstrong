from flask import Flask, request, jsonify
import math
import sys
from io import StringIO

app = Flask(__name__)

@app.route('/')
def home():
    return "🌌 Black Hole Physics API is live and running — use /blackhole endpoint!"

@app.route('/blackhole')
def blackhole():
    # Redirect print output
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()

    # Constants
    G = 6.674e-11
    c = 3.0e8

    try:
        # Get parameters safely
        M = float(request.args.get('M', 0))
        r = float(request.args.get('r', 0))
        mode = request.args.get('mode', '0')  # 0=faller, 1=viewer
        t_value = float(request.args.get('time', 1))
        m = float(request.args.get('m', 1))
        h = float(request.args.get('h', 1))

        # Physics safety check
        if M <= 0 or r <= 0:
            raise ValueError("Mass and distance must be positive values.")

        r_s = (2 * G * M) / c**2
        if r <= r_s:
            raise ValueError("Distance must be greater than Schwarzschild radius.")

        print(f"Schwarzschild radius = {r_s} m")

        # Time dilation
        if mode == '0':  # viewer -> faller
            t_faller = t_value * math.sqrt(1 - r_s / r)
            print(f"Faller's time = {t_faller} s")
        else:  # faller -> viewer
            t_viewer = t_value / math.sqrt(1 - r_s / r)
            print(f"Viewer's time = {t_viewer} s")

        # Escape velocity
        v_escape = math.sqrt((2 * G * M) / r)
        print(f"Escape velocity = {v_escape} m/s")

        # Gravitational acceleration
        g_acc = (G * M) / (r**2)
        print(f"Gravitational acceleration = {g_acc} m/s²")

        # Orbital velocity
        v_orb = math.sqrt((G * M) / r)
        print(f"Orbital velocity = {v_orb} m/s")

        # Gravitational redshift
        redshift = (1 / math.sqrt(1 - (r_s / r))) - 1
        print(f"Gravitational redshift = {redshift}")

        # Gravitational potential energy
        U = -((G * m * M) / r)
        print(f"Gravitational potential energy = {U} J")

        # Hover acceleration
        hover_a = (G * M / r**2) * math.sqrt(1 - (r_s / r))
        print(f"Hover acceleration = {hover_a} m/s²")

        # Orbital period
        T = 2 * math.pi * math.sqrt(r**3 / (G * M))
        print(f"Orbital period = {T} s")

        # Tidal force
        F_tidal = (2 * G * M * h) / (r**3)
        print(f"Tidal force = {F_tidal} N")

        # Restore stdout
        sys.stdout = old_stdout

        # Combine text and JSON for frontend
        output_text = mystdout.getvalue()
        data = {
            "Schwarzschild_radius": r_s,
            "Escape_velocity": v_escape,
            "Gravitational_acceleration": g_acc,
            "Orbital_velocity": v_orb,
            "Gravitational_redshift": redshift,
            "Potential_energy": U,
            "Hover_acceleration": hover_a,
            "Orbital_period": T,
            "Tidal_force": F_tidal,
        }

        if mode == '0':
            data["Faller_time"] = t_faller
        else:
            data["Viewer_time"] = t_viewer

        return jsonify({
            "text_output": output_text,
            "data": data
        })

    except ValueError as e:
        sys.stdout = old_stdout
        return jsonify({"error": str(e)})

    except Exception as e:
        sys.stdout = old_stdout
        return jsonify({"error": "Unexpected error: " + str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
