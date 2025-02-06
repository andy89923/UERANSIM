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
SERVER_URI = f"http://{SERVER_IP}:{SERVER_PORT}"

transmitting = True


def _receive_data(udp_socket):
    global transmitting

    # non-blocking receive
    udp_socket.settimeout(1)
    while True and transmitting:
        try:
            data, _ = udp_socket.recvfrom(2000)
            print(f"[DEBG] received data: {len(data)} bytes")
        except socket.timeout:
            pass


def __main__():
    global transmitting
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("127.0.0.1", 5001))

    data = {
        "src": "127.0.0.1",
        "MaxRate": "1M",
        "AvgRate": "2M",
        "MinRate": "3M",
    }
    session = session_for_src_addr("127.0.0.1")
    udp_thread = threading.Thread(target=_receive_data, args=(udp_socket,))
    udp_thread.start()

    try:
        r = session.post(f"{SERVER_URI}/start-traffic", json=data, timeout=3)
        if r.status_code == 200:
            print(f"[INFO] Traffic started")
        else:
            print(f"[ERROR] Traffic failed to start")
    except Exception as e:
        print(f"[ERROR] Traffic failed to start: {e}")

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

    udp_thread.join()


if __name__ == "__main__":
    __main__()
