#! /usr/bin/python3

import subprocess
import time
import signal
import threading
import os

UE_BINARY = "./../build/nr-ue"
NR_CLI_BINARY = "./../build/nr-cli"

class UE:
    
    supi = None # EX: imsi-208930000000001
    process = None
    
    def __init__(self, supi):
        self.supi = supi
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
            print(f"\n\n===============\n[INFO] UE {self.supi} received SIGINT")
            self.deregister()
            self.stop()
            
        signal.signal(signal.SIGINT, handler)
    
    
    def start(self):
        print(f"[INFO] Starting UE {self.supi}")
        
        if not self.authenticate():
            return
        
        print(f"[INFO] UE {self.supi} is running")
        self.process.wait()
        
        print(f"[INFO] UE {self.supi} has stopped")
        

    def stop(self):
        print(f"[INFO] Stopping UE {self.supi}")
        
        # delete config file
        subprocess.run(["rm", f"{self.config_file}"])
        self.process.send_signal(signal.SIGINT)
    
    
    def authenticate(self) -> bool:
        print(f"[INFO] UE: {self.supi} Authenticating")
        
        try:
            self.process = subprocess.Popen(
                [f"{UE_BINARY}", "-c", f"{self.config_file}"],
                preexec_fn=os.setpgrp) # Ignore SIGINT in the child process
        except Exception as e:
            print(f"Error: {e}")
            return False
        return True
    
    
    def deregister(self):
        print(f"[INFO] UE: {self.supi} Deregistering")
        
        subprocess.run([f"{NR_CLI_BINARY}", f"{self.supi}", "-e", "deregister switch-off"])
        
        print(f"[INFO] UE: {self.supi} Deregistered, waiting 2 seconds")
        time.sleep(2)
    

def __main__():
    ue1 = UE("imsi-208930000008888")
    ue1.start()
    
    
if __name__ == "__main__":
    __main__()