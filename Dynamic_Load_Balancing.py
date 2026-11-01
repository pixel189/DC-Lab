"""
Dynamic Load Balancing - Round-Robin & Least-Connections

HOW TO RUN IN EXAM:
 1. Open Notepad, copy ONLY the CSV lines below (between the two markers).
 2. File > Save As > Save as type: "All Files" > name: workload_5.csv
    (save in the SAME folder as this .py file)
 3. In VS Code terminal run:  python Dynamic_Load_Balancing.py
 4. Change DOMAIN and CSV_FILE below to match your chit.

CSV FILE NAME: workload_5.csv
------------ COPY FROM NEXT LINE ------------
job_id,compute_units,assigned_worker,status
J101,35,UNASSIGNED,PENDING
J102,80,UNASSIGNED,PENDING
J103,20,UNASSIGNED,PENDING
J104,60,UNASSIGNED,PENDING
J105,45,UNASSIGNED,PENDING
J106,10,UNASSIGNED,PENDING
J107,70,UNASSIGNED,PENDING
J108,25,UNASSIGNED,PENDING
------------ COPY TILL PREVIOUS LINE --------
"""

# ================= COMMON PART (same in all 10 programs) =================
import csv

DOMAIN   = "TrustMesh: Blockchain-Enabled Trusted IoT Framework"   # change per chit
CSV_FILE = "workload_5.csv"                                                  # change per chit

with open(CSV_FILE) as f:
    rows = list(csv.DictReader(f))       # rows = list of dicts, one dict per CSV row

print("=== Dynamic Load Balancer | " + DOMAIN + " ===")
print(f"Loaded {len(rows)} rows from {CSV_FILE}\n")
# ================= ONLY THE PART BELOW CHANGES =================
WORKERS = ["Worker_1", "Worker_2", "Worker_3"]

def balance(algo):
    load  = {w: 0 for w in WORKERS}
    conns = {w: 0 for w in WORKERS}
    rr = 0
    print(f"\n########## {algo} ##########")
    for job in rows:
        units = int(job["compute_units"])
        if algo == "ROUND-ROBIN":
            worker = WORKERS[rr % len(WORKERS)]
            rr += 1
        else:                                   # LEAST-CONNECTIONS
            worker = min(WORKERS, key=lambda w: (conns[w], load[w]))
        load[worker] += units
        conns[worker] += 1
        job["assigned_worker"], job["status"] = worker, "ASSIGNED"
        print(f"[ALLOCATE] {job['job_id']} ({units} units) -> {worker}")
        print("           load:", {w: f"{conns[w]} jobs/{load[w]} units" for w in WORKERS})
    print(f"--- Summary ({algo}) ---")
    for w in WORKERS:
        print(f"{w}: {conns[w]} jobs, {load[w]} units")

balance("ROUND-ROBIN")
balance("LEAST-CONNECTIONS")
