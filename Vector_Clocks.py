"""
Vector Clocks - Detecting Concurrency vs Causal Dependencies

HOW TO RUN IN EXAM:
 1. Open Notepad, copy ONLY the CSV lines below (between the two markers).
 2. File > Save As > Save as type: "All Files" > name: vector_events_6.csv
    (save in the SAME folder as this .py file)
 3. In VS Code terminal run:  python Vector_Clocks.py
 4. Change DOMAIN and CSV_FILE below to match your chit.

CSV FILE NAME: vector_events_6.csv
------------ COPY FROM NEXT LINE ------------
event_id,process_id,event_action,target_process
E1,P1,SEND,P2
E2,P2,RECEIVE,P1
E3,P3,LOCAL,-
E4,P2,SEND,P3
E5,P3,RECEIVE,P2
E6,P1,LOCAL,-
------------ COPY TILL PREVIOUS LINE --------
"""

# ================= COMMON PART (same in all 10 programs) =================
import csv

DOMAIN   = "TrustMesh: Blockchain-Enabled Trusted IoT Framework"   # change per chit
CSV_FILE = "vector_events_6.csv"                                                  # change per chit

with open(CSV_FILE) as f:
    rows = list(csv.DictReader(f))       # rows = list of dicts, one dict per CSV row

print("=== Vector Clocks | " + DOMAIN + " ===")
print(f"Loaded {len(rows)} rows from {CSV_FILE}\n")
# ================= ONLY THE PART BELOW CHANGES =================
from collections import defaultdict

procs   = ["P1", "P2", "P3"]
idx     = {p: i for i, p in enumerate(procs)}
vc      = {p: [0, 0, 0] for p in procs}
pending = defaultdict(list)
events  = []

for r in rows:
    p, act, eid = r["process_id"], r["event_action"].upper(), r["event_id"]
    i = idx[p]
    if act == "SEND":
        vc[p][i] += 1
        pending[r["target_process"]].append((p, vc[p][:]))
    elif act == "RECEIVE":
        if pending[p]:
            sender, mv = pending[p].pop(0)
            vc[p] = [max(a, b) for a, b in zip(vc[p], mv)]     # element-wise max
        vc[p][i] += 1
    else:
        vc[p][i] += 1
    events.append((eid, vc[p][:]))
    print(f"{eid} {p} {act:7} -> {vc[p]}")

def happens_before(a, b):
    return all(x <= y for x, y in zip(a, b)) and a != b

print("\n=== PAIRWISE COMPARISON ===")
for i in range(len(events)):
    for j in range(i + 1, len(events)):
        (e1, v1), (e2, v2) = events[i], events[j]
        if happens_before(v1, v2):
            print(f"{e1} {v1} < {e2} {v2} : Causally Preceding ({e1} -> {e2})")
        elif happens_before(v2, v1):
            print(f"{e2} {v2} < {e1} {v1} : Causally Preceding ({e2} -> {e1})")
        else:
            print(f"{e1} {v1} || {e2} {v2} : Concurrent")
