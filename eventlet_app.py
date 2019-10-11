"""Web server module."""

import eventlet
eventlet.monkey_patch()

import traceback
import zmq
from threading import Lock
from flask import Flask, render_template
from flask_socketio import SocketIO, emit, Namespace
import eventlet
from eventlet.greenpool import GreenPool
from zmq.error import ZMQError

pool = GreenPool(size=1000)


def background_thread(socket):

    """Get status info from ZeroMq, this is blocking function."""
    print("Thread started")
    try:
        print('Okinuo bt')
        print(type(socket))
        while not socket.closed:
            try:
                eventlet.sleep(1)
                res = socket.recv_string(flags=zmq.NOBLOCK)
                print('Status info recieved: ', res)
                socketio.emit('status_subscription', res, namespace="/status")
            except ZMQError as e:
                pass
    except Exception as e:
        traceback.print_exc()
        return ""
    print("Thread finished")


app = Flask(__name__)
socketio = SocketIO(async_mode="eventlet")
socketio.init_app(app)

thread = None
thread_lock = Lock()

context = zmq.Context()
zmq_main_socket = context.socket(zmq.REQ)
zmq_main_socket.connect("tcp://localhost:5555")


def create_listening_socket():
    zmq_status_socket = context.socket(zmq.SUB)
    zmq_status_socket.setsockopt_string(zmq.SUBSCRIBE, "")
    zmq_status_socket.connect("tcp://localhost:5556")
    return zmq_status_socket


def run_app():
    app.run(debug=False)


@app.route('/')
def home():
    """Home route."""
    return render_template('main.html')


@app.route('/')
def second():
    """Second route."""
    return render_template('second.html')


@socketio.on('some_event', namespace='/app')
def some_event(message):
    """WebSocket event handler"""
    print('Some event occured')
    encoded = 'data'.encode('utf-8')
    zmq_main_socket.send(encoded)
    response = zmq_main_socket.recv()
    emit('some_event_response', response.decode('utf-8'))


@socketio.on('some_event2', namespace='/app')
def some_event(message):
    """WebSocket event handler"""
    print('Some event 2 occured')
    encoded = 'data'.encode('utf-8')
    zmq_main_socket.send(encoded)
    response = zmq_main_socket.recv()
    emit('some_event_response2', response.decode('utf-8'))


class MyNamespace(Namespace):

    def on_connect(self):
        print("Starting connection")
        self.socket = create_listening_socket()
        self.worker = pool.spawn(background_thread, self.socket)
        emit('my_response', {'data': 'Connected', 'count': 0})
        print("Connected")

    def on_disconnect(self):
        print("Server disconnected")
        self.socket.close()
        self.worker.wait()


socketio.on_namespace(MyNamespace('/status'))


if __name__ == '__main__':
    app.run(debug=False)
