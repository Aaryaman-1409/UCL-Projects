import unittest
from scripts.tools import zeromq_client
import zmq, time
from threading import Thread
from collections import deque
import json
from random import randint
import os
import time

zeromq_port = zeromq_client.zeromq_port

context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.setsockopt(zmq.SNDHWM, 20)
socket.setsockopt(zmq.RCVHWM, 20)


class TestZeroMQ(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        socket.bind(f"tcp://127.0.0.1:{zeromq_port}")
        zeromq_client.zeromq_receiver_thread.start()
        zeromq_client.zeromq_sender_thread.start()
        
    def test_server_to_client(self):
        # Test if specific message goes through from server to client
        i = randint(1, 100)
        socket.send_json(json.dumps({"test": i}))
        
        # We start a while loop since the message might take some time to reach
        result = None
        while result is None:
            result = zeromq_client.receive_from_website()
            if result is None:
                continue
            assert(json.loads((result))["test"] == i)
    
    def test_server_to_client_multi(self):
        # Test if all messages go through without dropping from server to client
        for i in range(20):
            socket.send_json(json.dumps({"test": i}))
        
        results = []
        while len(results) < 20:
            result = zeromq_client.receive_from_website()
            if result is None:
                continue
            results.append(json.loads(result)["test"])
        
        assert(len(set(results)) == 20)

    def test_client_to_server(self):
        # Test if specific message goes through from client to server
        i = randint(1, 100)
        zeromq_client.send_to_website(json.dumps({"test": i}))

        assert(json.loads((socket.recv_json()))["test"] == i)

    def test_client_to_server_multi(self):
        # Test if all messages go through without dropping from client to server
        for i in range(20):
            zeromq_client.send_to_website(json.dumps({"test": i}))
        
        results = []
        while len(results) < 20:
            result = socket.recv_json()
            # Ignore keepalive message
            if "type" in result:
                continue
            results.append(json.loads(result)["test"])
        
        assert(len(set(results)) == 20)

    def test_keepalive(self):
        # Test if keepalive messages are received
        while True:
            # We don't send any message from the client, so all we should receive keepalives
            result = socket.recv_json()
            first_keepalive = result

            result = socket.recv_json()
            second_keepalive = result
            break
        
        # Check if we receive the same keepalive message
        assert(first_keepalive == second_keepalive)

    def test_keepalive_interval(self):
        # Test if keepalive messages are received 1 second apart, and no more
        while True:
            # We don't send any message from the client, so all we should receive are keepalives
            _ = socket.recv_json()
            first_keepalive_time = time.time()

            _ = socket.recv_json()
            second_keepalive_time = time.time()
            break
        
        # Check if we receive keepalives with a one second gap
        assert(round(second_keepalive_time - first_keepalive_time) == 1)

if __name__ == "__main__":
    unittest.main()