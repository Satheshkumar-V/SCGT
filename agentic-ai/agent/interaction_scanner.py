from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/parse', methods=['POST'])
def parse_logs():
    log = request.json.get("logData", "")
    return jsonify({
        "contact_name": "Satheshkumar",
        "role": "Researcher",
        "interaction_type": "email",
        "summary": "Discussion about AI trends",
        "timestamp": "2025-06-20T10:30:00Z"
    })

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
