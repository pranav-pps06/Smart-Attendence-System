from flask import Flask, render_template, request, redirect, url_for, session, send_file, jsonify
import os
import pandas as pd
from fpdf import FPDF
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecret'

USERNAME = "admin"
PASSWORD = "pranavps06"

status_file = "status.txt"
data_file = "attendance_data/attendance.csv"

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == USERNAME and request.form['password'] == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    with open(status_file, 'r') as f:
        status = f.read().strip()
    return render_template('dashboard.html', status=status)

@app.route('/toggle/<state>')
def toggle(state):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    with open(status_file, 'w') as f:
        f.write(state)
    return redirect(url_for('dashboard'))

@app.route('/status')
def status():
    try:
        with open(status_file, 'r') as f:
            return f.read().strip()
    except:
        return "off"

@app.route('/submit_attendance', methods=['POST'])
def submit_attendance():
    data = request.get_json()
    name = data.get("name")
    timestamp = data.get("timestamp")

    if not name or not timestamp or name.strip().lower() == "unknown":
        return jsonify({"error": "Invalid or unknown name"}), 400

    date_col = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").date().isoformat()

    # Load or create attendance DataFrame
    if os.path.exists(data_file):
        df = pd.read_csv(data_file)
    else:
        df = pd.DataFrame(columns=["Name"])

    # Ensure name exists in the file
    if name not in df["Name"].values:
        df.loc[len(df)] = [name] + ["A"] * (len(df.columns) - 1)

    # Add new date column if not present, and mark all as Absent
    if date_col not in df.columns:
        df[date_col] = "A"

    # Mark this name as Present
    df.loc[df["Name"] == name, date_col] = "P"

    df.to_csv(data_file, index=False)
    print(f"Marked {name} as present on {date_col}")
    return jsonify({"message": "Attendance recorded"}), 200

@app.route('/download_pdf')
def download_pdf():
    df = pd.read_csv(data_file)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)

    # Title
    pdf.cell(200, 10, txt="Attendance Report", ln=True, align='C')
    pdf.ln(10)

    # Auto column width
    col_count = len(df.columns)
    col_width = 190 / col_count if col_count else 190

    # Header
    for col in df.columns:
        pdf.cell(col_width, 10, txt=col, border=1, align='C')
    pdf.ln()

    # Rows
    for _, row in df.iterrows():
        for item in row:
            pdf.cell(col_width, 10, txt=str(item), border=1, align='C')
        pdf.ln()

    output_path = "attendance_data/attendance.pdf"
    pdf.output(output_path)
    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    os.makedirs("attendance_data", exist_ok=True)

    # Init CSV if needed
    if not os.path.exists(data_file):
        if os.path.exists("names.txt"):
            with open("names.txt") as f:
                names = [line.strip() for line in f if line.strip()]
        else:
            names = []
        df_init = pd.DataFrame({"Name": names})
        df_init.to_csv(data_file, index=False)

    if not os.path.exists(status_file):
        with open(status_file, 'w') as f:
            f.write("off")

    app.run(host='0.0.0.0', port=5000)
