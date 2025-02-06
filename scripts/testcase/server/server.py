#! /usr/bin/sudo /usr/bin/python3

from flask import Flask, request, jsonify
import threading
import time
import socket
import random

LISTEN_PORT = 2163
CLIENT_PORT = 5001
LISTEN_IP = "0.0.0.0"

app = Flask(__name__)
traffic_threads = {}
traffic_events = {}

RAND_SEED = 163
random.seed(RAND_SEED)


# Simulate starting traffic for a specific UE by sending UDP packets
def start_traffic(ue_ip, max_rate, avg_rate, min_rate):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    target_port = CLIENT_PORT
    while traffic_events[ue_ip].is_set():
        # Generate a random bitrate within the range
        bitrate = int(random.uniform(min_rate, max_rate))
        packet_size = bitrate // 8  # Convert bits per second to bytes per second
        packet_data = b"X" * packet_size

        # split the packet data into 1496 bytes
        packet_data = [
            packet_data[i : i + 1496] for i in range(0, len(packet_data), 1496)
        ]
        for data in packet_data:
            try:
                udp_socket.sendto(data, (ue_ip, target_port))
            except Exception as e:
                print(f"Error sending packet to {ue_ip}: {e}")
                pass
        print(f"Sent {packet_size} bytes to UE {ue_ip} at bitrate {bitrate} bps")
        time.sleep(1)  # Send packets every second

    udp_socket.close()


# string bitrate to int
def bitrate_to_int(bitrate):
    if "M" in bitrate:
        return int(bitrate.replace("M", "")) * 1000000
    elif "K" in bitrate:
        return int(bitrate.replace("K", "")) * 1000
    else:
        return int(bitrate)


@app.route("/start-traffic", methods=["POST"])
def traffic_start():
    data = request.get_json()
    ue_ip = data.get("src")
    max_rate = bitrate_to_int(data.get("MaxRate"))
    avg_rate = bitrate_to_int(data.get("AvgRate"))
    min_rate = bitrate_to_int(data.get("MinRate"))

    if not ue_ip or max_rate is None or min_rate is None:
        return (
            jsonify({"error": "Missing required parameters: src, MaxRate, MinRate"}),
            400,
        )

    if ue_ip in traffic_events and traffic_events[ue_ip].is_set():
        return jsonify({"message": f"Traffic is already running for UE {ue_ip}."}), 200

    traffic_events[ue_ip] = threading.Event()
    traffic_events[ue_ip].set()
    traffic_threads[ue_ip] = threading.Thread(
        target=start_traffic, args=(ue_ip, max_rate, avg_rate, min_rate)
    )
    traffic_threads[ue_ip].start()

    return jsonify({"message": f"Traffic started for UE {ue_ip}."}), 200


@app.route("/stop-traffic", methods=["POST"])
def traffic_stop():
    data = request.get_json()
    ue_ip = data.get("src")

    if not ue_ip:
        return jsonify({"error": "Missing required parameter: src"}), 400

    if ue_ip not in traffic_events or not traffic_events[ue_ip].is_set():
        return jsonify({"message": f"Traffic is already stopped for UE {ue_ip}."}), 200

    traffic_events[ue_ip].clear()
    traffic_threads[ue_ip].join()
    del traffic_threads[ue_ip]
    del traffic_events[ue_ip]

    return jsonify({"message": f"Traffic stopped for UE {ue_ip}."}), 200


if __name__ == "__main__":
    app.run(host=LISTEN_IP, port=LISTEN_PORT)
