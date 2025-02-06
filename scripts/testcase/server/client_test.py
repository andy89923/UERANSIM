#! /usr/bin/sudo /usr/bin/python3

import socket
import threading
import time


# session.py
import requests
import requests.adapters


def session_for_src_addr(addr: str):
    session = requests.Session()
    for prefix in ["http://", "https://"]:
        adapter = session.get_adapter(prefix)
        adapter.init_poolmanager(
            connections=requests.adapters.DEFAULT_POOLSIZE,
            maxsize=requests.adapters.DEFAULT_POOLSIZE,
            source_address=(addr, 0),
        )
        adapter.timeout = 3
    return session


# End of session.py

SERVER_IP = "140.113.208.88"
SERVER_PORT = 2163
CLIENT_PORT = 5001
SERVER_URI = f"http://{SERVER_IP}:{SERVER_PORT}"

transmitting = True


def _receive_data(tcp_socket):
    global transmitting

    # Connect to the server
    tcp_socket.connect((SERVER_IP, CLIENT_PORT))
    print(f"[INFO] Connected to server")

    # send data
    tcp_socket.send("127.0.0.1".encode())

    while True and transmitting:
        try:
            data = tcp_socket.recv(2000)
            if data:
                pass
                # print(f"[DEBG] received data: {len(data)} bytes")
            else:
                break
        except Exception as e:
            pass


def __main__():
    global transmitting
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.bind(("140.113.208.88", 5002))

    data = {
        "src": "127.0.0.1",
        "MaxRate": "1M",
        "AvgRate": "2M",
        "MinRate": "3M",
    }
    session = session_for_src_addr("127.0.0.1")

    tcp_thread = threading.Thread(target=_receive_data, args=(tcp_socket,))
    try:
        r = session.post(f"{SERVER_URI}/start-traffic", json=data, timeout=3)
        if r.status_code == 200:
            print(f"[INFO] Traffic started")
            tcp_thread.start()
        else:
            print(f"[ERROR] Traffic failed to start")
            return
    except Exception as e:
        print(f"[ERROR] Traffic failed to start: {e}")
        return

    time.sleep(10)

    data = {
        "src": "127.0.0.1",
    }
    try:
        r = session.post(f"{SERVER_URI}/stop-traffic", json=data, timeout=3)
        if r.status_code == 200:
            transmitting = False
            print(f"[INFO] Traffic stopped")
    except Exception as e:
        print(f"[ERROR] Traffic failed to stop: {e}")

    tcp_thread.join()


if __name__ == "__main__":
    __main__()
