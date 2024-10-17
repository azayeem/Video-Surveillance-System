from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")


@app.route('/alert', methods=['POST'])
def alert():
    data = request.json
    # Process the alert and send notification to mobile app
    send_notification(data)
    print(data)
    return jsonify({"status": "success"}), 200


def send_notification(data):
    # Logic to send notification to mobile app
    socketio.emit('alert', data)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)


# flask run --host=192.168.1.42 --port=5000
# flask run --host=192.168.100.26 --port=5000
