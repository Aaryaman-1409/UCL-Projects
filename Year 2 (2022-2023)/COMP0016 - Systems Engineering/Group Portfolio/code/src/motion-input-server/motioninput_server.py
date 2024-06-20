import asyncio, time, psutil, zmq
from collections import deque
from threading import Thread
import websockets.server
from websockets.server import WebSocketServerProtocol
from pathlib import Path
from subprocess import Popen
import json


def receive_from_zeromq():
    while True:
        message = socket.recv_json()
        print(message)
        mi_to_website_queue.append(message)
        rest()


def send_to_zeromq():
    while True:
        try:
            data = website_to_mi_queue.pop()
            socket.send_json(data)
        except IndexError:
            pass
        finally:
            rest()


async def send_to_websocket(websocket: WebSocketServerProtocol):
    last_keepalive = time.time()
    while True:
        try:
            data = mi_to_website_queue.pop()
            last_keepalive = time.time()
            await websocket.send(data)
        except IndexError:
            if (time.time() - last_keepalive) > 5:
                keepalive_message = json.dumps({"type": {"mi_status": "disconnected"}})
                last_keepalive = time.time()
                await websocket.send(keepalive_message)
        finally:
            rest()
            # asyncio.sleep forcefully yields to event loop in case the message buffer isn't large enough
            await asyncio.sleep(0)


async def receive_from_websocket(websocket: WebSocketServerProtocol):
    async for message in websocket:
        json_message = json.loads(message)
        command = json_message.get("type", {}).get("command", None)
        mi_config = json_message.get("type", {}).get("mi_config", None)

        if command == "Relaunch MotionInput":
            start_motion_input()

        if mi_config is not None:
            website_to_mi_queue.append(json_message)

        rest()


async def websocket_handler(websocket: WebSocketServerProtocol):
    await asyncio.gather(
        send_to_websocket(websocket), receive_from_websocket(websocket)
    )


async def serve_websocket():
    async with websockets.server.serve(websocket_handler, "localhost", websocket_port):
        await asyncio.Future()  # this await will never be fulfilled, so the context manager will remain open


def start_motion_input():
    motion_input_filename = "motioninput_api.exe"
    dir_path = Path(__file__).parent.parent / "MotionInput"
    print(dir_path)
    if motion_input_filename not in (p.name() for p in psutil.process_iter()):
        motion_input_path = dir_path / motion_input_filename
        print(motion_input_filename)
        Popen(motion_input_path)
    else:
        print("Akready running")


# sleeps are necessary to keep CPU usage low when polling sockets. Adjust the sleep interval here. Larger sleeps mean lower CPU usage, 
# but worse performance. 0.001 appears to be the sweet spot
def rest():
    time.sleep(0.001)


websocket_port = 5786
zeromq_port = 8435

context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.setsockopt(zmq.SNDHWM, 20)
socket.setsockopt(zmq.RCVHWM, 20)
socket.bind(f"tcp://127.0.0.1:{zeromq_port}")

zeromq_sender_thread = Thread(target=send_to_zeromq, daemon=True)
zeromq_receiver_thread = Thread(target=receive_from_zeromq, daemon=True)

mi_to_website_queue = deque(maxlen=40)
website_to_mi_queue = deque(maxlen=40)

if __name__ == "__main__":
    zeromq_sender_thread.start()
    zeromq_receiver_thread.start()
    asyncio.run(serve_websocket())
