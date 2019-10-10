"""Web server module."""

import traceback
import zmq
import time
import gevent
from threading import Lock
from flask import Flask, render_template, Response
from flask_socketio import SocketIO, emit, Namespace
from flask_apscheduler import APScheduler


def background_thread():
    """Get status info from ZeroMq, this is blocking function."""
    try:
        print('Okinuo bt')
        while True:
            res = zmq_status_socket.recv_string()
            print('Status info recieved: ', res)
            socketio.emit('status_subscription', res, namespace="/status")
            socketio.sleep(1)
    except:
        traceback.print_exc()
        return ""


# class Config(object):
#     JOBS = [
#         {
#             'id': 'read_status_info',
#             'func': 'application:read_status_info',
#         }
#     ]

#     SCHEDULER_API_ENABLED = True

app = Flask(__name__)
# app.config.from_object(Config())
socketio = SocketIO(async_mode=None)
socketio.init_app(app)
# scheduler = APScheduler()
# scheduler.init_app(app)
# scheduler.start()

thread = None
thread_lock = Lock()


context = zmq.Context()
zmq_main_socket = context.socket(zmq.REQ)
zmq_main_socket.connect("tcp://localhost:5555")
zmq_status_socket = context.socket(zmq.SUB)
zmq_status_socket.setsockopt_string(zmq.SUBSCRIBE, "")
zmq_status_socket.connect("tcp://localhost:5556")


def run_app():
    app.run(debug=False)


@app.route('/')
def home():
    """Home route."""
    return render_template('main.html')


@socketio.on('some_event', namespace='/app')
def some_event(message):
    """WebSocket event handler"""
    print('Some event occured')
    encoded = 'data'.encode('utf-8')
    zmq_main_socket.send(encoded)
    response = zmq_main_socket.recv()
    emit('some_event_response', response.decode('utf-8'))


class MyNamespace(Namespace):
    def on_connect(self):
        global thread
        with thread_lock:
            if thread is None:
                thread = socketio.start_background_task(background_thread)
        emit('my_response', {'data': 'Connected', 'count': 0})


socketio.on_namespace(MyNamespace('/status'))


if __name__ == '__main__':
    app.run(debug=False)
