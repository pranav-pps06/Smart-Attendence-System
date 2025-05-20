from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Initial LED state
led_state = 'off'

@app.route('/')
def index():
    return render_template('index.html', led_state=led_state)

@app.route('/toggle', methods=['POST'])
def toggle():
    global led_state
    action = request.form.get('action')
    if action in ['on', 'off']:
        led_state = action
        return jsonify({'status': 'success', 'led_state': led_state})
    return jsonify({'status': 'error', 'message': 'Invalid action'}), 400

@app.route('/status')
def status():
    return led_state

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
