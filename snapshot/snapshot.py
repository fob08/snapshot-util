"""
Make snapshot

{"Tasks": {"total": 440, "running": 1, "sleeping": 354, "stopped": 1, "zombie": 0},
"%CPU": {"user": 14.4, "system": 2.2, "idle": 82.7},
"KiB Mem": {"total": 16280636, "free": 335140, "used": 11621308},
"KiB Swap": {"total": 16280636, "free": 335140, "used": 11621308},
"Timestamp": 1624400255}
"""
import time
import os
import argparse
import psutil
import json

class SystemMonitor:

    def __init__(self,interval,output_filename,snapshot_quantity):
        self.interval = interval
        self.output_filename = output_filename
        self.snapshot_quantity = snapshot_quantity

    def tracker(self):
        task = {
           "total": len(psutil.pids()),
           "running": len([p for p in psutil.process_iter() if p.status() == psutil.STATUS_RUNNING]),
           "sleeping": len([p for p in psutil.process_iter() if p.status() == psutil.STATUS_SLEEPING]),
           "stopped": len([p for p in psutil.process_iter() if p.status() == psutil.STATUS_STOPPED]),
           "zombie": len([p for p in psutil.process_iter() if p.status == psutil.STATUS_ZOMBIE]),
        }
          
        cpu = psutil.cpu_times_percent(interval=None)

        cpu_mem = {
            "user": cpu.user,
            "system": cpu.system,
            "idle": cpu.idle,
            }
        
        memory = psutil.virtual_memory()

        mem = {
            "total": memory.total,
            "free": memory.free,
            "used": memory.used,
        }

        swapmem = psutil.swap_memory()

        swap = {
            "total": swapmem.total,
            "free": swapmem.free,
            "used": swapmem.used,
        }

        timestamp = int(time.time())

        snapshot = {
            "Tasks": task,
            "%CPU": cpu_mem,
            "KiB Mem": mem,
            "KiB Swap": swap,
            "Timestamp": timestamp,
        }
        return snapshot
    
    def write_snapshot(self, snapshot):
        with open(self.output_filename, "a") as file:
            json.dump(snapshot, file)
            file.write("\n")
    
    def clear_output_file(self):
        with open(self.output_filename, "w") as file:
            file.write("")

    def monitor(self):
        self.clear_output_file()
        for _ in range(self.snapshot_quantity):
            snapshot =self.tracker()
            os.system('clear')
            print(json.dumps(snapshot, indent=4), end="\r")
            self.write_snapshot(snapshot)
            time.sleep(self.interval)

def main():
    """Snapshot tool."""
   
  
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help="Interval between snapshots in seconds", type=int, default=30)
    parser.add_argument("-f", help="Output file name", default="snapshot.json")
    parser.add_argument("-n", help="Quantity of snapshot to output", default=20)
    args = parser.parse_args()

    monitor = SystemMonitor(args.i, args.f, args.n)
    monitor.monitor()


if __name__ == "__main__":
    main()