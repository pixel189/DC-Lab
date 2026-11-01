"""
Multithreading - Concurrent Processing & Mutex/Lock Synchronization

HOW TO RUN IN EXAM:
 1. Open Notepad, copy ONLY the CSV lines below (between the two markers).
 2. File > Save As > Save as type: "All Files" > name: tasks_4.csv
    (save in the SAME folder as this .py file)
 3. In VS Code terminal run:  python Multithreading.py
 4. Change DOMAIN and CSV_FILE below to match your chit.

CSV FILE NAME: tasks_4.csv
------------ COPY FROM NEXT LINE ------------
task_id,thread_name,burst_ms,priority,status
T1,Worker_1,200,HIGH,PENDING
T2,Worker_2,150,LOW,PENDING
T3,Worker_1,100,MEDIUM,PENDING
T4,Worker_3,250,HIGH,PENDING
T5,Worker_2,120,HIGH,PENDING
T6,Worker_3,80,LOW,PENDING
------------ COPY TILL PREVIOUS LINE --------
"""

# ================= COMMON PART (same in all 10 programs) =================
import csv

DOMAIN   = "TrustMesh: Blockchain-Enabled Trusted IoT Framework"   # change per chit
CSV_FILE = "tasks_4.csv"                                                  # change per chit

with open(CSV_FILE) as f:
    rows = list(csv.DictReader(f))       # rows = list of dicts, one dict per CSV row

print("=== Multithreading with Mutex | " + DOMAIN + " ===")
print(f"Loaded {len(rows)} rows from {CSV_FILE}\n")
# ================= ONLY THE PART BELOW CHANGES =================
import threading, time
from collections import defaultdict

lock = threading.Lock()          # MUTEX
completed_tasks = []             # shared list
total_burst = 0                  # shared counter

def worker(name, tasks):
    global total_burst
    for t in tasks:
        print(f"[{name}] STARTED {t['task_id']} (burst={t['burst_ms']}ms, priority={t['priority']})")
        time.sleep(int(t["burst_ms"]) / 1000)
        lock.acquire()
        print(f"[{name}] >>> LOCK ACQUIRED ({t['task_id']})")
        try:
            temp = total_burst
            time.sleep(0.01)                       # would cause a race WITHOUT the lock
            total_burst = temp + int(t["burst_ms"])
            t["status"] = "COMPLETED"
            completed_tasks.append((t["task_id"], name, t["priority"]))
        finally:
            print(f"[{name}] <<< LOCK RELEASED ({t['task_id']})")
            lock.release()

groups = defaultdict(list)
for r in rows:
    groups[r["thread_name"]].append(r)
order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
for g in groups.values():
    g.sort(key=lambda r: order.get(r["priority"], 3))

threads = [threading.Thread(target=worker, args=(n, tl)) for n, tl in groups.items()]
for th in threads: th.start()
for th in threads: th.join()

print("\n=== FINAL COMPLETED TASK LIST ===")
for tid, name, pr in completed_tasks:
    print(f"{tid} | {name} | {pr} | COMPLETED")
expected = sum(int(r["burst_ms"]) for r in rows)
print(f"\nShared total = {total_burst} ms (expected {expected}) -> "
      f"{'NO RACE CONDITION' if total_burst == expected else 'RACE DETECTED'}")
