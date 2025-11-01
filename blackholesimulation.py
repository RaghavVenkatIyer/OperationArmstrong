# app.py
import os
import math
import sys
from io import StringIO
from flask import Flask, request, Response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allow cross-origin requests; install flask_cors if required

G = 6.674e-11
c = 3.0e8

def safe_float(val, name=None):
    try:
        return float(val)
    except (TypeError, ValueError):
        raise ValueError(f"Parameter '{name}' must be a valid number.")

@app.route('/')
def home():
    return "🌌 Black Hole Physics API is live and running — use /blackhole endpoint!"

@app.route('/blackhole')
def blackhole():
    # capture output into a string (keeps your front-end display logic)
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()

    try:
        # Read query params
        M_raw = request.args.get('M', None)
        r_raw = request.args.get('r', None)
        mode = request.args.get('time', request.args.get('mode', '0'))  # accept either param name
        t_raw = request.args.get('time_value', request.args.get('time', None))  # optional
        # length and other optional params
        lengthselection = request.args.get('lengthselection', None)
        viewerslength_raw = request.args.get('viewerslength', None)
        fallerslength_raw = request.args.get('fallerslength', None)
        m_raw = request.args.get('m', request.args.get('objectmass', None))
        h_raw = request.args.get('h', request.args.get('height', None))

        # Required param checks
        if M_raw is None or r_raw is None:
            raise ValueError("Missing required parameters: 'M' (mass) and 'r' (distance).")

        # Parse numeric params
        M = safe_float(M_raw, 'M')
        r = safe_float(r_raw, 'r')
        t_value = None
        if t_raw is not None:
            t_value = safe_float(t_raw, 'time')

        m_obj = safe_float(m_raw, 'm') if m_raw is not None else None
        h = safe_float(h_raw, 'h') if h_raw is not None else None

        # Validate physical values
        if M <= 0 or r <= 0:
            raise ValueError("Mass 'M' and distance 'r' must be positive numbers.")

        # Schwarzschild radius
        r_s = (2 * G * M) / (c ** 2)
        print(f"Schwarzschild radius = {r_s} m")

        if r <= r_s:
            raise ValueError("Distance 'r' must be greater than the Schwarzschild radius (r_s).")

        # Time dilation: if mode parameter is provided use it; default to 0 behavior if t_value provided
        # mode: '0' means viewer -> faller (viewer time provided), '1' means faller -> viewer (faller time provided)
        if mode is None:
            mode = '0'

        if t_value is None:
            # If user didn't provide a time, we will skip time-dilation conversion but still compute other properties
            print("No time value provided; skipping time-dilation conversion.")
        else:
            if mode == '0' or mode == 'viewer' or mode == 'v':
                # viewer time given, compute faller time
                if (1 - r_s / r) < 0:
                    raise ValueError("Invalid geometry: (1 - r_s / r) < 0. Distance is too close to horizon.")
                t_faller = t_value * math.sqrt(1 - r_s / r)
                print(f"Given viewer's time = {t_value} s → Faller's time = {t_faller} s")
            else:
                # faller time given, compute viewer time
                if (1 - r_s / r) <= 0:
                    raise ValueError("Invalid geometry: (1 - r_s / r) <= 0. Distance is too close to horizon.")
                t_viewer = t_value / math.sqrt(1 - r_s / r)
                print(f"Given faller's time = {t_value} s → Viewer's time = {t_viewer} s")

        # Escape velocity
        v_escape = math.sqrt((2 * G * M) / r)
        print(f"Escape velocity = {v_escape} m/s")

        # Gravitational acceleration
        g_acc = (G * M) / (r ** 2)
        print(f"Gravitational acceleration = {g_acc} m/s²")

        # Orbital velocity
        v_orb = math.sqrt((G * M) / r)
        print(f"Orbital velocity = {v_orb} m/s")

        # Gravitational redshift
        redshift = (1 / math.sqrt(1 - (r_s / r))) - 1
        print(f"Gravitational redshift = {redshift}")

        # Compressed length (if provided)
        if lengthselection is not None:
            try:
                ls = int(lengthselection)
            except:
                ls = None
            if ls == 0 and viewerslength_raw is not None:
                viewers_len = safe_float(viewerslength_raw, 'viewerslength')
                faller_len = viewers_len * math.sqrt(1 - (r_s / r))
                print(f"Viewer's length = {viewers_len} m → Faller's length = {faller_len} m")
            elif ls == 1 and fallerslength_raw is not None:
                faller_len = safe_float(fallerslength_raw, 'fallerslength')
                viewers_len = faller_len / math.sqrt(1 - (r_s / r))
                print(f"Faller's length = {faller_len} m → Viewer's length = {viewers_len} m")
            else:
                print("Length selection provided but required length value missing; skipping length conversion.")

        # Gravitational potential energy (if object mass provided)
        if m_obj is not None:
            U = -((G * m_obj * M) / r)
            print(f"Gravitational potential energy (m={m_obj} kg) = {U} J")
        else:
            print("No object mass 'm' provided; skipping gravitational potential energy.")

        # Hover acceleration
        hover_a = (G * M / r ** 2) * math.sqrt(1 - (r_s / r))
        print(f"Hover acceleration = {hover_a} m/s²")

        # Orbital period
        T = 2 * math.pi * math.sqrt(r ** 3 / (G * M))
        print(f"Orbital period = {T} s")

        # Tidal force (if height provided)
        if h is not None:
            F_tidal = (2 * G * M * h) / (r ** 3)
            print(f"Tidal force (for height {h} m) = {F_tidal} N")
        else:
            print("No height 'h' provided; skipping tidal force calculation.")

        # Summary
        print("\nSummary:")
        print(f"Schwarzschild radius: {r_s} m")
        print(f"Escape velocity: {v_escape} m/s")
        print(f"Gravitational acceleration: {g_acc} m/s²")
        print(f"Orbital velocity: {v_orb} m/s")
        print(f"Gravitational redshift: {redshift}")

        sys.stdout = old_stdout
        text = mystdout.getvalue()
        return Response(f"<pre>{text}</pre>", mimetype='text/html')

    except ValueError as ve:
        sys.stdout = old_stdout
        return Response(f"<pre>Error: {ve}</pre>", mimetype='text/html'), 400

    except Exception as e:
        sys.stdout = old_stdout
        return Response(f"<pre>Unexpected error: {e}</pre>", mimetype='text/html'), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
