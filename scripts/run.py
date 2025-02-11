#! /usr/bin/sudo /usr/bin/python3

RAND_SEED = 163
DATA_SET_FILE = "testcase/sample.json"

from models import dataset
from colorama import Fore, Style
from ue import UE
import threading
import time

COL = Fore.CYAN
END = Style.RESET_ALL

app_map = {}


def ue_thread(ueConfig):
    global app_map

    print(f"{COL}[Info] Starting UE {ueConfig.IMSI}{END}")
    print(ueConfig)

    ue = UE(ueConfig)

    # Start UE when it arrives (Arrival_Time)
    print(
        f"{COL}[Info] Waiting for UE {ueConfig.IMSI} to arrive at {ueConfig.Arrival_Time}{END}"
    )
    time.sleep(ueConfig.Arrival_Time)

    ueThread = threading.Thread(target=ue.start)
    ueThread.start()

    # Start UE according to the configuration
    timer = ueConfig.Arrival_Time
    for app in ueConfig.AppInterval:
        print(
            f"{COL}[Info] Starting App {app_map[app.Id].Description} at {app.start_time} for UE {ueConfig.IMSI}{END}"
        )
        time.sleep(app.start_time - timer)
        timer = app.start_time

        # Start app
        ue.startTraffic(app_map[app.Id])

        # End app
        print(
            f"{COL}[Info] Ending App {app_map[app.Id].Description} at {app.end_time} for UE {ueConfig.IMSI}{END}"
        )
        time.sleep(app.end_time - timer)
        timer = app.end_time
        ue.stopTraffic()

    # Wait for UE to leave
    print(
        f"{COL}[Info] Waiting for UE {ueConfig.IMSI} to leave at {ueConfig.Leave_Time}{END}"
    )
    time.sleep(ueConfig.Leave_Time - timer)
    ue.deregister()
    ue.stop()

    print(f"{COL}[Info] UE {ueConfig.IMSI} has left{END}")
    ueThread.join()


def __main__():
    print(f"{COL}Starting Simulation{END}")
    global app_map

    # read file from json
    with open(DATA_SET_FILE, "r") as f:
        rawdata = f.read()
        f.close()

    # create dataset object
    data = dataset.Dataset()
    data.from_json(rawdata)

    print(f"{COL}Using Dataset: {data.Name}{END}")

    # Application Map
    for app in data.Application:
        app_map[app.Id] = app

    # UE threads
    threads = []
    for ue in data.UE:
        # Create UE thread
        t = threading.Thread(target=ue_thread, args=(ue,))
        threads.append(t)

    # Start threads
    print(f"{COL}Starting {len(threads)} UE threads{END}")
    for t in threads:
        t.start()

    # Wait for threads to finish
    print(f"{COL}Waiting for UE threads to finish{END}")
    for t in threads:
        t.join()

    print(f"{Fore.GREEN}Simulation Finished{END}")


if __name__ == "__main__":
    __main__()
