"""
Author: Aaryaman Sharma
"""

import time
import json
import zmq
from collections import deque
from threading import Thread


# Importing module in python is cached, so the queue is essentially a singleton that can be shared among modules


def send_to_zeromq():
    last_keepalive = time.time()
    while True:
        try:
            data = mi_to_website_queue.pop()
            last_keepalive = time.time()
            socket.send_json(data)
        except IndexError:
            if (time.time() - last_keepalive) > 1:
                keepalive_message = json.dumps({"type": {"mi_status": "connected"}})
                last_keepalive = time.time()
                socket.send_json(keepalive_message)
        finally:
            rest()


def receive_from_zeromq():
    while True:
        message = socket.recv_json()
        website_to_mi_queue.append(message)
        rest()


# sleeps are necessary to keep CPU usage low when polling sockets. Adjust the sleep interval here. Larger sleeps mean lower CPU usage, 
# but worse performance. 0.001 appears to be the sweet spot
def rest():
    time.sleep(0.001)


def start_thread():
    zeromq_sender_thread.start()
    zeromq_receiver_thread.start()


# User facing APIs.
def send_to_website(data):
    mi_to_website_queue.append(data)


def receive_from_website():
    try:
        return website_to_mi_queue.pop()
    except IndexError:
        return None


zeromq_port = 8435
context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.setsockopt(zmq.SNDHWM, 20)
socket.setsockopt(zmq.RCVHWM, 20)
socket.connect(f"tcp://localhost:{zeromq_port}")

# Set queue length to around double the zeromq send and receive limits
# to minimize dropped messages
mi_to_website_queue = deque(maxlen=40)
website_to_mi_queue = deque(maxlen=40)
zeromq_sender_thread = Thread(target=send_to_zeromq, daemon=True)
zeromq_receiver_thread = Thread(target=receive_from_zeromq, daemon=True)
