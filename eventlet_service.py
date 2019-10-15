"""Service module."""
import traceback
import zmq
import eventlet
from eventlet.greenpool import GreenPool
from random import randint
from json import dumps


pool = GreenPool(size=1000)
context = zmq.Context()
socket_responder = context.socket(zmq.REP)
socket_responder.bind("tcp://*:5555")
socket_publisher = context.socket(zmq.PUB)
socket_publisher.bind("tcp://*:5556")
socket_tasker = context.socket(zmq.PUB)
socket_tasker.bind("tcp://*:5557")


def long_task():
    """Long task simulation."""
    print('Long task execution starting.')
    for i in range(0, 30):
        print(i)
        eventlet.sleep(1)
    print('Waited 30 secnods.')
    data = {
        "val": 999
    }
    response = dumps(data).encode('utf-8')
    socket_tasker.send(response)
    print('Responded', response)


def respond_recieve():
    """Respond on request."""
    data = 0
    while True:
        eventlet.sleep(0)
        try:
            message = socket_responder.recv(zmq.NOBLOCK)
            print(message)
            print('Spawning long task now..')
            pool.spawn(long_task)
            response = str(data).encode('utf-8')
            socket_responder.send(response)
            data += 1
        except:
            pass


def publisher():
    """Publish new data to server."""
    while True:
        eventlet.sleep(1)
        try:
            data = {
                'number_1': randint(0, 1000),
                'number_2': randint(1000, 2000)
            }
            json_data = dumps(data)
            socket_publisher.send_string(json_data)
            print('Published system info.')
        except:
            traceback.print_exc()


pool.spawn(respond_recieve)
pool.spawn(publisher)
pool.waitall()
