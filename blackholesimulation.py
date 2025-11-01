from flask import Flask, request
import math
import sys
from io import StringIO

app = Flask(__name__)

@app.route('/')
def home():
    return "🌌 Black Hole Physics API is live and running — use /blackhole endpoint!"

@app.route('/blackhole')
def blackhole():
    # Redirect print output to a string
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()

    # Safe input replacement system
    input_values = []
    def fake_input(prompt=''):
        if not input_values:
            raise ValueError("Error: pop from empty list — missing input.")
        return input_values.pop(0)
    global input
    input = fake_input

    # Collect query params
    params = request.args
    M = params.get('M')
    r = params.get('r')
    time_mode = params.get('time')
    viewerstime = params.get('viewerstime')
    fallerstime = params.get('fallerstime')
    lengthselection = params.get('lengthselection')
    viewerslength = params.get('viewerslength')
    fallerslength = params.get('fallerslength')
    m = params.get('m')
    h = params.get('h')

    # Prepare fake input list
    input_values = [v for v in [M, r, time_mode] if v not in [None, ""]]
    if time_mode == "0" and viewerstime:
        input_values.append(viewerstime)
    elif time_mode == "1" and fallerstime:
        input_values.append(fallerstime)
    if lengthselection:
        input_values.append(lengthselection)
        if lengthselection == "0" and viewerslength:
            input_values.append(viewerslength)
        elif lengthselection == "1" and fallerslength:
            input_values.append(fallerslength)
    if m:
        input_values.append(m)
    if h:
        input_values.append(h)

    # Constants
    G = 6.674e-11
    c = 3.0e8

    # ==================== BEGIN CALCULATIONS ====================
    M = float(input("Enter the mass of black hole (kilograms): "))
    r = float(input("Enter the distance of the person from the black hole (meters): "))
    r_s = (2 * G * M) / c**2
    print(f"Schwarzschild radius (r_s): {r_s:.15f} m")

    if r <= r_s:
        raise ValueError(f"❌ Distance r ({r}) must be greater than Schwarzschild radius ({r_s}).")

    mode = int(input("Enter 0 for faller’s time (input viewer’s time), or 1 for viewer’s time (input faller’s time): "))
    if mode == 0:
        viewerstime = float(input("Enter the viewer's time (seconds): "))
        t_faller = viewerstime * math.sqrt(1 - r_s / r)
        print(f"Faller’s proper time: {t_faller:.15f} seconds")
    else:
        fallerstime = float(input("Enter the faller’s time (seconds): "))
        t_viewer = fallerstime / math.sqrt(1 - r_s / r)
        print(f"Viewer’s time dilation: {t_viewer:.15f} seconds")

    escapevelocity = math.sqrt((2 * G * M) / r)
    gravitationalacceleration = (G * M) / (r**2)
    orbitalvelocity = math.sqrt((G * M) / r)
    gravitationalredshift = (1 / math.sqrt(1 - (r_s / r))) - 1

    print(f"Escape velocity: {escapevelocity:.15f} m/s")
    print(f"Gravitational acceleration: {gravitationalacceleration:.15f} m/s²")
    print(f"Orbital velocity: {orbitalvelocity:.15f} m/s")
    print(f"Gravitational redshift: {gravitationalredshift:.15f}")

    # Length contraction
    print("\n📏 Length Contraction Engine")
    lengthselection = int(input("Enter 0 if providing viewers length, enter 1 if providing fallers length: "))
    if lengthselection == 0:
        viewersleng = float(input("Enter the viewer’s length (m): "))
        fallerslength = viewersleng * math.sqrt(1 - (r_s / r))
        print(f"Faller’s length: {fallerslength:.15f} m")
    else:
        fallerslen = float(input("Enter the faller’s length (m): "))
        viewerslength = fallerslen / math.sqrt(1 - (r_s / r))
        print(f"Viewer’s length: {viewerslength:.15f} m")

    # Gravitational potential energy
    print("\n⚡ Gravitational Potential Energy Engine")
    m = float(input("Enter the mass of the object near the black hole (kg): "))
    gravitationalpotentialenergy = -((G * m * M) / r)
    print(f"Gravitational potential energy: {gravitationalpotentialenergy:.15f} J")

    # Acceleration required to hover
    print("\n🚀 Hover Acceleration Calculator")
    acceleration = G * M / r**2 * math.sqrt(1 - (r_s / r))
    print(f"Required hover acceleration: {acceleration:.15f} m/s²")

    # Orbital period
    print("\n🪐 Orbital Period Calculator")
    orbitalperiod = 2 * math.pi * math.sqrt(r**3 / (G * M))
    print(f"Orbital period: {orbitalperiod:.15f} s")

    # Tidal force
    print("\n🌊 Tidal Force Calculator")
    h = float(input("Enter the person’s height (m): "))
    tidalforce = (2 * G * M * h) / (r**3)
    print(f"Tidal force difference: {tidalforce:.15f} N/kg")

    print("\n✅ All calculations complete — summary of results:")
    print(f"r_s = {r_s:.15f}")
    print(f"Escape velocity = {escapevelocity:.15f}")
    print(f"Gravitational acceleration = {gravitationalacceleration:.15f}")
    print(f"Orbital velocity = {orbitalvelocity:.15f}")
    print(f"Redshift = {gravitationalredshift:.15f}")
    print(f"GPE = {gravitationalpotentialenergy:.15f}")
    print(f"Hover acceleration = {acceleration:.15f}")
    print(f"Orbital period = {orbitalperiod:.15f}")
    print(f"Tidal force = {tidalforce:.15f}")

    # ==================== END CALCULATIONS ====================

    sys.stdout = old_stdout
    return f"<pre>{mystdout.getvalue()}</pre>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
