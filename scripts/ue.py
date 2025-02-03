#! /usr/bin/sudo /usr/bin/python3

import subprocess
import time
import signal
import os
from colorama import Fore, Style

UE_BINARY = "./../build/nr-ue"
NR_CLI_BINARY = "./../build/nr-cli"

SEPARATOR = "=" * 80


class UE:
    supi = None  # EX: imsi-208930000000001
    process = None

    def __init__(self, supi):
        self.supi = supi
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

        # SIGINT
        def handler(signum, frame):
            print(
                f"\n\n{SEPARATOR}\n{Fore.YELLOW}[INFO] UE {self.supi} received SIGINT{Style.RESET_ALL}"
            )
            self.deregister()
            self.stop()

        signal.signal(signal.SIGINT, handler)

    def start(self):
        print(f"[INFO] Starting UE {self.supi}")

        if not self.authenticate():
            return

        print(f"[INFO] UE {self.supi} is running")

        # Connection setup for PDU session[1] is successful, TUN interface[uesimtun0, 10.60.0.3] is up
        # stdout, _ = self.process.communicate()

        with self.process.stdout:
            for line in iter(self.process.stdout.readline, ""):
                if line.strip() == b"":
                    break
                msg = line.strip().decode("utf-8")
                print(msg)
                if "Connection setup for PDU session[1] is successful" in msg:
                    self.ip = msg.split(",")[2].split(" ")[1].split("]")[0]
                    self.tunnel = msg.split(",")[1].split("[")[1]
                    print(f"{SEPARATOR}")
                    # Add color to the output
                    print(
                        f"{Fore.GREEN}[INFO] UE {self.supi} is connected to {self.ip} via {self.tunnel}{Style.RESET_ALL}"
                    )
                    print(f"{SEPARATOR}")

        self.process.wait()

        print(f"{Fore.RED}[INFO] UE {self.supi} has stopped")

    def stop(self):
        print(f"[INFO] Stopping UE {self.supi}")

        # delete config file
        subprocess.run(["rm", f"{self.config_file}"])
        self.process.send_signal(signal.SIGINT)

    def authenticate(self) -> bool:
        print(f"[INFO] UE: {self.supi} Authenticating")

        try:
            # Ignore SIGINT in the child process
            # preexec_fn=os.setpgrp
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


def __main__():
    ue1 = UE("imsi-208930000008888")
    ue1.start()


if __name__ == "__main__":
    __main__()
