from flask import Flask, request, jsonify
import math
import numpy as np
import sys
from io import StringIO
import plotly.graph_objects as go

app = Flask(__name__)

@app.route('/')
def home():
    return "🌌 Black Hole Physics API with Plotly Graphs is live — use /blackhole endpoint!"

@app.route('/blackhole')
def blackhole():
    # redirect print()
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()

    # constants
    G = 6.674e-11
    c = 3.0e8

    try:
        # Read parameters
        M = float(request.args.get('M', 0))
        r = float(request.args.get('r', 0))
        mode = request.args.get('mode', '0')  # 0=faller, 1=viewer
        t_value = float(request.args.get('time', 1))
        m = float(request.args.get('m', 1))
        h = float(request.args.get('h', 1))

        # Safety validations
        if M <= 0 or r <= 0:
            raise ValueError("Mass and distance must be positive.")

        r_s = (2 * G * M) / c**2
        if r <= r_s:
            raise ValueError("Distance must be greater than Schwarzschild radius.")

        print(f"Schwarzschild radius = {r_s} m")

        # Time dilation formulas
        if mode == '0':  # viewer → faller time
            t_faller = t_value * math.sqrt(1 - r_s / r)
            print(f"Faller's time = {t_faller} s")
        else:           # faller → viewer time
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

        # Potential energy
        U = -((G * m * M) / r)
        print(f"Gravitational potential energy = {U} J")

        # Hover acceleration
        hover_a = (G * M) / (r**2 * math.sqrt(1 - r_s / r))
        print(f"Hover acceleration = {hover_a} m/s²")

        # Orbital period
        T = 2 * math.pi * math.sqrt(r**3 / (G * M))
        print(f"Orbital period = {T} s")

        # Tidal force
        F_tidal = (2 * G * M * h) / (r**3)
        print(f"Tidal force = {F_tidal} N")

        # -------------------------
        #   PLOTLY GRAPH SECTION
        # -------------------------
        r_values = np.linspace(r_s * 1.1, r * 3, 300)

        # 1. Escape velocity graph
        escape_curve = np.sqrt((2 * G * M) / r_values)
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=r_values, y=escape_curve, mode='lines'))
        fig1.update_layout(title="Escape Velocity vs Distance",
                           xaxis_title="Distance (m)",
                           yaxis_title="Escape Velocity (m/s)")
        fig1.write_html("escape_velocity_graph.html")

        # 2. Gravitational redshift graph
        redshift_curve = (1 / np.sqrt(1 - (r_s / r_values))) - 1
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=r_values, y=redshift_curve, mode='lines'))
        fig2.update_layout(title="Gravitational Redshift vs Distance",
                           xaxis_title="Distance (m)",
                           yaxis_title="Redshift (dimensionless)")
        fig2.write_html("gravitational_redshift_graph.html")

        # 3. Time dilation graph
        dtau_curve = np.sqrt(1 - 3 * G * M / (r_values * c**2))
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=r_values, y=dtau_curve, mode='lines'))
        fig3.update_layout(title="Time Dilation (dtau/dt) vs Distance",
                           xaxis_title="Distance (m)",
                           yaxis_title="Time Dilation Factor")
        fig3.write_html("timedilation_graph.html")

        print("\nGraphs generated successfully:")
        print(" - escape_velocity_graph.html")
        print(" - gravitational_redshift_graph.html")
        print(" - timedilation_graph.html")

        # Restore stdout for JSON output
        sys.stdout = old_stdout
        output_text = mystdout.getvalue()

        # JSON response object
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
            "Graph_files": [
                "escape_velocity_graph.html",
                "gravitational_redshift_graph.html",
                "timedilation_graph.html"
            ]
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


# Run on Replit
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
