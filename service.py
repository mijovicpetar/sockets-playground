"""Service module."""

import traceback
import gevent
import zmq
import random
import sys
import time
from random import randint
from json import dumps


context = zmq.Context()

socket_responder = context.socket(zmq.REP)
socket_responder.bind("tcp://*:5555")

socket_publisher = context.socket(zmq.PUB)
socket_publisher.bind("tcp://*:5556")


def respond_recieve():
    """Respond on request."""
    data = 0
    while True:
        gevent.sleep(0)
        try:
            message = socket_responder.recv(zmq.NOBLOCK)
            response = str(data).encode('utf-8')
            socket_responder.send(response)
            print('Responded', response)
            data += 1
        except:
            pass


def publisher():
    """Publish new data to server."""
    while True:
        gevent.sleep(1)
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


gevent.joinall([
    gevent.spawn(respond_recieve),
    gevent.spawn(publisher)
])
