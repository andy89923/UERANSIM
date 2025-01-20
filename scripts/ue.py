#! /usr/bin/python3

import subprocess
import atexit

UE_BINARY = "./../build/nr-ue"

class UE:
    
    supi = None # EX: imsi-208930000000001
    
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
        
    def start(self):
        print(f"Starting UE {self.supi}")
        
        atexit.register(self.stop)
        self.authenticate()
        
    def stop(self):
        print(f"Stopping UE {self.supi}")
        
        # delete config file
        subprocess.run(["rm", f"{self.config_file}"])
    
    def authenticate(self):
        print(f"UE: {self.supi} Authenticating")
        
        # run shell code 
        subprocess.run([f"{UE_BINARY}", "-c", f"{self.config_file}"])
        
    

def __main__():
    ue1 = UE("imsi-208930000008888")
    ue1.start()
    
    
if __name__ == "__main__":
    __main__()