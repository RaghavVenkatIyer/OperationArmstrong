from flask import Flask, request, jsonify
import math

app = Flask(__name__)

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.json
        M = float(data.get('mass'))
        r = float(data.get('distance'))
        time_mode = int(data.get('mode'))  # 0 = faller’s time, 1 = viewer’s time
        time_value = float(data.get('time'))

        # === YOUR ORIGINAL CODE (unchanged logic) ===
        G = 6.674e-11
        c = 3.0e8
        rinmeters = (10**-3) * r
        r_s = (2 * G * M) / c**2

        if time_mode == 0:
            # viewers time given, calculate faller’s time
            viewerstime = time_value
            t_faller = viewerstime * math.sqrt(1 - r_s / rinmeters)
            result = {
                "schwarzchild_radius": r_s,
                "faller_time": t_faller
            }
        else:
            # faller’s time given, calculate viewer’s time
            fallerstime = time_value
            t_viewer = fallerstime / math.sqrt(1 - r_s / rinmeters)
            result = {
                "schwarzchild_radius": r_s,
                "viewer_time": t_viewer
            }

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/')
def home():
    return "✅ Black Hole Time Dilation API is running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
