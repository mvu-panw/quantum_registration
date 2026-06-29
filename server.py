from flask import Flask, request, jsonify, send_from_directory
import csv, os
from datetime import datetime, timezone

app = Flask(__name__, static_folder='.', static_url_path='')
CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'registrations.csv')

def ensure_csv():
    if not os.path.exists(CSV_PATH):
        with open(CSV_PATH, 'w', newline='') as f:
            csv.writer(f).writerow(['timestamp', 'name', 'email', 'company'])

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/register', methods=['POST'])
def register():
    data    = request.get_json(silent=True) or {}
    name    = (data.get('name') or '').strip()
    email   = (data.get('email') or '').strip().lower()
    company = (data.get('company') or '').strip()
    if not (name and email and company):
        return jsonify({'status': 'error', 'message': 'Missing fields'}), 400
    ensure_csv()
    with open(CSV_PATH, 'a', newline='') as f:
        csv.writer(f).writerow([datetime.now(timezone.utc).isoformat(), name, email, company])
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    ensure_csv()
    app.run(port=3535, debug=True)
