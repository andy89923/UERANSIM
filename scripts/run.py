#! /usr/bin/python3.12

RAND_SEED = 163
DATA_SET_FILE = "testcase/sample.json"

from models import dataset
import threading

from models.ue import UserEquipment
from ue import UE

import time

app_map = {}


def ue_thread(ueConfig):
    global app_map

    print(f"[Info] Starting UE {ueConfig.IMSI}")
    print(ueConfig)

    ue = UE(ueConfig)

    # Start UE when it arrives (Arrival_Time)
    print(f"[Info] Waiting for UE {ueConfig.IMSI} to arrive at {ueConfig.Arrival_Time}")
    time.sleep(ueConfig.Arrival_Time)

    ue.start()

    # Start UE according to the configuration
    timer = ueConfig.Arrival_Time
    for app in ueConfig.AppInterval:
        print(f"[Info] Starting App {app_map[app.Id].Name} at {app.start_time}")
        time.sleep(app.start_time - timer)
        timer = app.start_time

        # Start app
        ue.startTraffic(app_map[app.Id])

        # End app
        print(f"[Info] Ending App {app_map[app.Id].Name} at {app.end_time}")
        time.sleep(app.end_time - timer)
        timer = app.end_time
        ue.stopTraffic()

    # Wait for UE to leave
    print(f"[Info] Waiting for UE {ueConfig.IMSI} to leave at {ueConfig.Leave_Time}")
    time.sleep(ueConfig.Leave_Time - timer)
    ue.deregister()
    ue.stop()


def __main__():
    global app_map

    # read file from json
    with open(DATA_SET_FILE, "r") as f:
        rawdata = f.read()
        f.close()

    # create dataset object
    data = dataset.Dataset()
    data.from_json(rawdata)

    print(f"Using Dataset: {data.Name}")

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
    for t in threads:
        t.start()

    for t in threads:
        t.join()


if __name__ == "__main__":
    __main__()
