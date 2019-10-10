"""Service module."""

import threading
import traceback
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
        time.sleep(1)
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


respond_recieve_thread = threading.Thread(target=respond_recieve)
publisher_thread = threading.Thread(target=publisher)

respond_recieve_thread.start()
publisher_thread.start()
