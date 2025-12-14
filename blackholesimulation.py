from flask import Flask, request, jsonify, send_from_directory
import math
import numpy as np
import sys
from io import StringIO
import plotly.graph_objects as go
import os

app = Flask(__name__, static_url_path='', static_folder='.')

# ============================================================
#                       CONSTANTS
# ============================================================
G = 6.674e-11
c = 3.0e8


# Route for serving graph files
@app.route('/graphs/<path:filename>')
def serve_graphs(filename):
    return send_from_directory('.', filename)


@app.route('/')
def home():
    return "🌌 Black Hole Physics API Online — use /blackhole endpoint."


@app.route('/blackhole')
def blackhole():

    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()

    try:
        # ============================================================
        #                     READ PARAMETERS
        # ============================================================
        M = float(request.args.get('M', 0))
        r = float(request.args.get('r', 0))
        mode = request.args.get('mode', '0')
        t_value = float(request.args.get('time', 1))
        m = float(request.args.get('m', 1))
        h = float(request.args.get('h', 1))
        theta_deg = float(request.args.get('theta', 0))

        # ============================================================
        #                     VALIDATION
        # ============================================================
        if M <= 0 or r <= 0:
            raise ValueError("Mass and distance must be positive.")

        r_s = 2 * G * M / c**2
        if r <= r_s:
            raise ValueError("Distance must be greater than Schwarzschild radius.")

        print(f"Schwarzschild radius = {r_s} m")

        # ============================================================
        #                     TIME DILATION
        # ============================================================
        if mode == "0":
            t_faller = t_value * math.sqrt(1 - r_s / r)
            print(f"Faller time = {t_faller} s")
        else:
            t_viewer = t_value / math.sqrt(1 - r_s / r)
            print(f"Viewer time = {t_viewer} s")

        # ============================================================
        #                     BASIC GR CALCULATIONS
        # ============================================================
        escape_v = math.sqrt(2 * G * M / r)
        print(f"Escape velocity = {escape_v} m/s")

        g_acc = (G * M) / r**2
        print(f"Gravitational acceleration = {g_acc} m/s²")

        orbital_v = math.sqrt(G * M / r)
        print(f"Orbital velocity = {orbital_v} m/s")

        redshift = 1 / math.sqrt(1 - r_s / r) - 1
        print(f"Gravitational redshift = {redshift}")

        U = -(G * M * m) / r
        print(f"Potential energy = {U} J")

        hover_acc = (G * M) / (r**2 * math.sqrt(1 - r_s / r))
        print(f"Hover acceleration = {hover_acc} m/s²")

        orbital_period = 2 * math.pi * math.sqrt(r**3 / (G * M))
        print(f"Orbital period = {orbital_period} s")

        tidal_force = (2 * G * M * h) / (r**3)
        print(f"Tidal force = {tidal_force} N")

        # ============================================================
        #               DEFLECTION OF LIGHT (LENSING)
        # ============================================================
        alpha = 4 * G * M / (r * c**2)
        print(f"Light deflection angle = {alpha} radians")

        # ============================================================
        #               SHAPIRO TIME DELAY
        # ============================================================
        r1 = float(request.args.get("r1", r*10))
        r2 = float(request.args.get("r2", r*10))
        shapiro = (2 * G * M / c**3) * math.log((4 * r1 * r2) / (r**2))
        print(f"Shapiro delay = {shapiro} s")

        # ============================================================
        #               SPECIAL RELATIVISTIC EFFECTS
        # ============================================================
        dtau_dt = math.sqrt(1 - 3 * G * M / (r * c**2))
        print(f"GR time dilation dtau/dt = {dtau_dt}")

        omega = math.sqrt(G * M / r**3)
        v_local = (r * omega) / math.sqrt(1 - r_s / r)
        print(f"Local orbital velocity = {v_local} m/s")

        gamma = 1 / math.sqrt(1 - (v_local / c)**2)
        print(f"Lorentz factor gamma = {gamma}")

        theta = math.radians(theta_deg)
        g_factor = math.sqrt(1 - r_s / r) / (gamma * (1 - (v_local/c) * math.cos(theta)))
        print(f"Observed frequency shift g-factor = {g_factor}")

        # ============================================================
        #                        PLOTLY GRAPHS
        # ============================================================
        r_vals = np.linspace(r_s * 1.1, r * 3, 300)

        # Escape velocity graph
        esc_curve = np.sqrt(2 * G * M / r_vals)
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=r_vals, y=esc_curve))
        fig1.update_layout(title="Escape Velocity vs Distance")
        fig1.write_html("escape_velocity_graph.html")

        # Redshift graph
        red_curve = (1 / np.sqrt(1 - r_s / r_vals)) - 1
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=r_vals, y=red_curve))
        fig2.update_layout(title="Gravitational Redshift vs Distance")
        fig2.write_html("gravitational_redshift_graph.html")

        # Time dilation graph
        td_curve = np.sqrt(1 - 3 * G * M / (r_vals * c**2))
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=r_vals, y=td_curve))
        fig3.update_layout(title="Time Dilation vs Distance")
        fig3.write_html("timedilation_graph.html")

        # ============================================================
        #                      PREPARE JSON OUTPUT
        # ============================================================
        sys.stdout = old_stdout
        output_console = mystdout.getvalue()

        result = {
            "Schwarzschild_radius": r_s,
            "Escape_velocity": escape_v,
            "Gravitational_acceleration": g_acc,
            "Orbital_velocity": orbital_v,
            "Gravitational_redshift": redshift,
            "Potential_energy": U,
            "Hover_acceleration": hover_acc,
            "Orbital_period": orbital_period,
            "Tidal_force": tidal_force,
            "Deflection_angle": alpha,
            "Shapiro_delay": shapiro,
            "GR_time_dilation": dtau_dt,
            "Local_orbital_velocity": v_local,
            "Lorentz_gamma": gamma,
            "Frequency_shift_g_factor": g_factor,
            "Graph_links": {
                "escape": "/graphs/escape_velocity_graph.html",
                "redshift": "/graphs/gravitational_redshift_graph.html",
                "timedilation": "/graphs/timedilation_graph.html"
            },
            "console_output": output_console
        }

        if mode == "0":
            result["Faller_time"] = t_faller
        else:
            result["Viewer_time"] = t_viewer

        return jsonify(result)

    except Exception as e:
        sys.stdout = old_stdout
        return jsonify({"error": str(e)})


# Run on Replit
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81)
