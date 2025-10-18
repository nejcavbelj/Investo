"""
Minimal Flask test
"""

from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello World"

@app.route('/test', methods=['POST'])
def test():
    return jsonify({'success': True, 'message': 'Test successful'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
