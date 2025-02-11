#! /usr/bin/sudo /usr/bin/python3

import subprocess
import time
import signal
import os
from colorama import Fore, Style
import threading

import socket
from models import UserEquipment
from models import Application
from session import session_for_src_addr

UE_BINARY = "./../build/nr-ue"
NR_CLI_BINARY = "./../build/nr-cli"

SEPARATOR = "=" * 80

SERVER_IP = "140.113.208.88"
SERVER_PORT = 2163
SERVER_URI = f"http://{SERVER_IP}:{SERVER_PORT}"
CLIENT_PORT = 5001


class UE:
    supi = None  # EX: imsi-208930000000001
    process = None

    userActivity = None
    transmitting = False

    def __init__(self, ue: UserEquipment):
        self.supi = ue.IMSI
        self.ip = None
        self.tunnel = None
        self.config_file = f"ue-{self.supi}.yaml"

        # Build config file
        with open("base-ue.yaml", "r") as f:
            data = f.read()
            data = data.replace("PLACE-IMSI-HERE", self.supi)
            f.close()

        # Write to file
        with open(f"{self.config_file}", "w") as f:
            f.write(data)
            f.close()

    def _start_client_port(self):
        # Start UDP socker to receive data
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.bind((self.ip, 0))

        # Start thread to receive data
        self.tcp_thread = threading.Thread(target=self._receive_data)
        self.tcp_thread.start()

    def _receive_data(self):
        self.tcp_socket.connect((SERVER_IP, CLIENT_PORT))
        self.tcp_socket.send(f"{self.ip}".encode())
        while True:
            try:
                data = self.tcp_socket.recv(2000)
                if data:
                    # print(f"[DEBG] {self.ip} receive len {len(data)}")
                    pass
                else:
                    print(f"[DEBG] {self.ip} server closed!")
                    break
            except Exception as e:
                print(f"[ERROR] UE: {self.ip} failed to receive data: {e}")

    def start(self):
        print(f"[INFO] Starting UE {self.supi}")
        if not self.authenticate():
            return

        print(f"{Fore.GREEN}[INFO] UE {self.supi} is running{Style.RESET_ALL}")
        with self.process.stdout:
            for line in iter(self.process.stdout.readline, ""):
                if line.strip() == b"":
                    break
                msg = line.strip().decode("utf-8")
                print(msg)
                if "Connection setup for PDU session[1] is successful" in msg:
                    self.ip = msg.split(",")[2].split(" ")[1].split("]")[0]
                    self.tunnel = msg.split(",")[1].split("[")[1]
                    print(
                        f"{SEPARATOR}\n",
                        f"{Fore.GREEN}[INFO] UE {self.supi} is connected to {self.ip} via {self.tunnel}{Style.RESET_ALL}\n",
                        f"{SEPARATOR}",
                        sep="",
                    )
                    self.session = session_for_src_addr(self.ip)
                    self._start_client_port()

        self.process.wait()
        print(f"{Fore.RED}[INFO] UE {self.supi} has stopped{Style.RESET_ALL}")

    def stop(self):
        print(f"[INFO] Stopping UE {self.supi}")

        # delete config file
        subprocess.run(["rm", f"{self.config_file}"])
        self.process.send_signal(signal.SIGINT)

    def authenticate(self) -> bool:
        print(f"[INFO] UE: {self.supi} Authenticating")

        try:
            # Ignore SIGINT in the child process:
            #   preexec_fn=os.setpgrp
            self.process = subprocess.Popen(
                [f"{UE_BINARY}", "-c", f"{self.config_file}"],
                preexec_fn=os.setpgrp,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except Exception as e:
            print(f"Error: {e}")
            return False
        return True

    def deregister(self):
        print(f"[INFO] UE: {self.supi} Deregistering")
        subprocess.run(
            [f"{NR_CLI_BINARY}", f"{self.supi}", "-e", "deregister switch-off"]
        )
        print(f"[INFO] UE: {self.supi} Deregistered, waiting 2 seconds")
        time.sleep(2)

    def startTraffic(self, application: Application):
        if self.transmitting == True:
            print(
                f"{Fore.RED}[ERRO] UE: {self.supi} Traffic is already running{Style.RESET_ALL}"
            )
            return
        print(f"[INFO] UE: {self.supi} Starting Traffic")

        # Srart traffic
        # send data to the server via the tunnel interface
        data = {
            "src": f"{self.ip}",
            "MaxRate": application.MaxBR,
            "AvgRate": application.AvgBR,
            "MinRate": application.MinBR,
        }
        try:
            r = self.session.post(f"{SERVER_URI}/start-traffic", json=data, timeout=3)
            if r.status_code == 200:
                self.transmitting = True
                print(f"[INFO] UE: {self.supi} Traffic started")
            else:
                print(f"[ERROR] UE: {self.supi} Traffic failed to start")
        except Exception as e:
            print(f"[ERROR] UE: {self.supi} Traffic failed to start: {e}")

    def stopTraffic(self):
        if self.transmitting == False:
            return
        print(f"[INFO] UE: {self.supi} Stopping Traffic")

        # Stop traffic
        # send data to the server via the tunnel interface
        data = {
            "src": f"{self.ip}",
        }
        try:
            r = self.session.post(f"{SERVER_URI}/stop-traffic", json=data, timeout=3)
            if r.status_code == 200:
                self.transmitting = False
                print(f"[INFO] UE: {self.supi} Traffic stopped")
        except Exception as e:
            print(f"[ERROR] UE: {self.supi} Traffic failed to stop: {e}")


def __main__():
    ue1 = UE(UserEquipment(Id=1, IMSI="imsi-208930000008888"))

    # SIGINT
    def handler(signum, frame):
        print(
            f"\n\n{SEPARATOR}\n{Fore.YELLOW}[INFO] UE {ue1.supi} received SIGINT{Style.RESET_ALL}"
        )
        ue1.deregister()
        ue1.stop()

    signal.signal(signal.SIGINT, handler)

    # Start UE use threading to run in parallel
    thread = threading.Thread(target=ue1.start)
    thread.start()

    # Wait for UE to get IP
    time.sleep(5)
    if ue1.ip is None:
        thread.join()
        return

    print(f"{Fore.GREEN}[INFO] UE is running, start traffic{Style.RESET_ALL}")
    ue1.startTraffic(
        Application(Id=1, Description="FTP", MaxBR="10M", AvgBR="5M", MinBR="1M")
    )
    time.sleep(3)
    ue1.stopTraffic()

    thread.join()


if __name__ == "__main__":
    __main__()
