import docker
import logging
import threading
import time

client = docker.from_env()
ran = client.containers.get("ueransim")
SUPI1 = "imsi-208930000000001"
SUPI2 = "imsi-208930000000002"
count = 0


# Adding time measurement, by using thread time
class UE:
    def __init__(self, id):
        self.SUPI = id

    def start(self):
        authenticate(self.SUPI)

    def stop(self):
        switchOff(self.SUPI)


def switchOff(id):
    r = checkingStatus(id)
    if r == "UP":
        global count
        count += 1
        cmd = './nr-cli %s -e "deregister switch-off"' % id
        (c, r) = ran.exec_run(cmd)
        print("UE-%s Switch Off" % id)


def _authenticate(id):
    r = checkingStatus(id)
    if r == "OFF":
        cmd = "./nr-ue -c config/uecfg.yaml -i %s" % id
        print("UE-%s Authenticating" % id)
        ran.exec_run(cmd)


def authenticate(id):
    thread = threading.Thread(target=_authenticate, args=(id,))
    thread.start()


# return "OFF", "INIT", "UP", "IDLE"
def checkingStatus(id):
    cmd = './nr-cli %s -e "status"' % id
    (c, r) = ran.exec_run(cmd)
    if c != 0:
        return "OFF"
    if r.decode("utf-8").find("MM-REGISTERED/NORMAL-SERVICE") != -1:
        return "UP"
    if r.decode("utf-8").find("MM-REGISTER-INITIATED") != -1:
        return "INIT"
    if r.decode("utf-8").find("CM-IDLE") != -1:
        return "IDLE"
    print(r)
    return "WRONG"


def activeThread():
    num = threading.active_count() - 1
    print("There are %d active UE" % num)


UE1 = UE(SUPI1)
# UE2 = UE(SUPI2)
while True:
    activeThread()
    print(count)
    time.sleep(1)
    UE1.start()
    # UE2.start()
    time.sleep(1)
    UE1.stop()
# UE2.stop()
