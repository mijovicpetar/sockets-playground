"""Web server module."""

import traceback
import zmq
import time
from flask import Flask, render_template, Response
from flask_socketio import SocketIO, emit


app = Flask(__name__)
socketio = SocketIO()
socketio.init_app(app)
context = zmq.Context()
zmq_main_socket = context.socket(zmq.REQ)
zmq_main_socket.connect("tcp://localhost:5555")
zmq_status_socket = context.socket(zmq.SUB)
zmq_status_socket.setsockopt_string(zmq.SUBSCRIBE, "")
zmq_status_socket.connect("tcp://localhost:5556")


def sse_status_info():
    """Get status info from ZeroMq, this is blocking function."""
    try:
        # Recv string is blocking.
        res = zmq_status_socket.recv_string()
        print('Status info recieved: ', res)
        return res
    except:
        traceback.print_exc()
        return ""


@app.route('/')
def home():
    """Home route."""
    return render_template('main.html')


@app.route('/stream')
def stream_status_information():
    """SSE route."""
    def streamer():
        """Generator method."""
        while True:
            # This format is mandatory.
            yield 'data: {}\n\n'.format(sse_status_info())
    return Response(streamer(), mimetype="text/event-stream")


@socketio.on('some_event', namespace='/app')
def some_event(message):
    """WebSocket event handler"""
    print('Some event occured')
    encoded = 'data'.encode('utf-8')
    zmq_main_socket.send(encoded)
    response = zmq_main_socket.recv()
    emit('some_event_response', response.decode('utf-8'))


def create_app():
    return socketio


if __name__ == '__main__':
    app.run(debug=False)
