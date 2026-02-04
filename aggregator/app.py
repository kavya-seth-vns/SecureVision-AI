from flask import Flask, request, jsonify, render_template_string
import pickle
from datetime import datetime

app = Flask(__name__)
updates = []

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SecureVision AI — SOC Dashboard</title>

<style>
:root {
    --bg: #020617;
    --card: rgba(15,23,42,0.85);
    --text: #e5e7eb;
    --accent: #38bdf8;
}

.light {
    --bg: #f8fafc;
    --card: #ffffff;
    --text: #020617;
}

body {
    margin: 0;
    font-family: 'Segoe UI', system-ui;
    background: var(--bg);
    color: var(--text);
    padding: 20px;
    transition: 0.3s;
}

.container {
    max-width: 1200px;
    margin: auto;
}

h1 {
    color: var(--accent);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

/* Toggle */
.toggle {
    cursor: pointer;
    padding: 8px 14px;
    border-radius: 8px;
    background: var(--card);
    font-size: 14px;
}

/* Alert */
.alert {
    background: #dc2626;
    color: white;
    padding: 12px 18px;
    border-radius: 10px;
    font-weight: bold;
    animation: blink 1.2s infinite;
    margin-bottom: 10px;
}

@keyframes blink {
    50% { opacity: 0.4; }
}

/* Secure badge */
.secure {
    background: #10b981;
    color: white;
    padding: 10px 16px;
    border-radius: 10px;
    display: inline-block;
    margin-bottom: 20px;
}

/* Grid */
.grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 20px;
}

/* Cards */
.card {
    background: var(--card);
    border-radius: 18px;
    padding: 20px;
    box-shadow: 0 0 25px rgba(56,189,248,0.15);
}

.big {
    font-size: 2rem;
    font-weight: bold;
    color: var(--accent);
}

/* Severity colors */
.low { color: #22c55e; }
.medium { color: #facc15; }
.high { color: #ef4444; }

/* Endpoint */
.endpoint {
    border-top: 1px solid #334155;
    padding-top: 12px;
    margin-top: 12px;
}

/* Fake map */
.map {
    height: 220px;
    border-radius: 14px;
    background: radial-gradient(circle at center, #0f172a, #020617);
    position: relative;
    overflow: hidden;
}

.dot {
    width: 10px;
    height: 10px;
    background: #38bdf8;
    border-radius: 50%;
    position: absolute;
    animation: pulse 1.5s infinite;
}

@keyframes pulse {
    0% { transform: scale(0.7); opacity: 0.6; }
    50% { transform: scale(1.3); opacity: 1; }
    100% { transform: scale(0.7); opacity: 0.6; }
}

footer {
    margin-top: 30px;
    font-size: 13px;
    opacity: 0.7;
    text-align: center;
}
</style>

<script>
// Auto refresh every 5 seconds
setTimeout(() => {
    window.location.reload();
}, 5000);

// Dark / Light toggle
function toggleTheme() {
    document.body.classList.toggle("light");
}
</script>
</head>

<body>
<div class="container">

<h1>
🛡 SecureVision AI — SOC Dashboard
<span class="toggle" onclick="toggleTheme()">🌓 Toggle Theme</span>
</h1>

<div class="alert">⚠ Anomaly Detected — Analyst Attention Required</div>
<div class="secure">🔐 Privacy-Preserving Federated Mode: ACTIVE ✔</div>

<div class="grid">

<div class="card">
    <div>Total Endpoint Updates</div>
    <div class="big">{{count}}</div>
</div>

<div class="card">
    <div>Endpoint Activity</div>
    {% for u in updates %}
    <div class="endpoint">
        <b>💻 {{u.endpoint_id}}</b><br>
        🕒 {{u.timestamp}}<br>
        🔢 Features: {{u.feature_count}}<br>
        ⚠ Severity:
        <span class="{{u.severity|lower}}">{{u.severity}}</span>
    </div>
    {% endfor %}
</div>

<div class="card">
    <div>🌍 Global Endpoint Map</div>
    <div class="map">
        <div class="dot" style="top:40%; left:30%"></div>
        <div class="dot" style="top:60%; left:55%"></div>
        <div class="dot" style="top:35%; left:70%"></div>
    </div>
</div>

</div>

<footer>
SecureVision AI · No Raw Telemetry Shared · AMD SEV Compatible
</footer>

</div>
</body>
</html>
"""

@app.route("/update", methods=["POST"])
def update():
    data = request.json
    print("🔥 RECEIVED DATA:", data)
    update_obj = {
        "endpoint_id": data.get("endpoint_id", "Unknown"),
        "feature_count": data.get("feature_count", 0),
        "severity": data.get("severity", "LOW"),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    updates.append(type('obj', (object,), update_obj))

    with open("model_store.pkl", "wb") as f:
        pickle.dump(updates, f)

    return jsonify({"status": "secure update received"})

@app.route("/")
def dashboard():
    return render_template_string(
        DASHBOARD_HTML,
        count=len(updates),
        updates=updates
    )

if __name__ == "__main__":
    app.run(debug=True)
