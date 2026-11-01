"""
Lamport's Logical Clocks - Scalar Timestamps & Total Causal Ordering

HOW TO RUN IN EXAM:
 1. Open Notepad, copy ONLY the CSV lines below (between the two markers).
 2. File > Save As > Save as type: "All Files" > name: events_7.csv
    (save in the SAME folder as this .py file)
 3. In VS Code terminal run:  python Lamport_Logical_Clock.py
 4. Change DOMAIN and CSV_FILE below to match your chit.

CSV FILE NAME: events_7.csv
------------ COPY FROM NEXT LINE ------------
event_id,process_id,event_type,message_to,initial_clock
E1,P1,SEND,P2,0
E2,P2,LOCAL,-,0
E3,P2,RECEIVE,P1,0
E4,P3,LOCAL,-,0
E5,P2,SEND,P3,0
E6,P3,RECEIVE,P2,0
E7,P1,LOCAL,-,0
E8,P3,SEND,P1,0
E9,P1,RECEIVE,P3,0
------------ COPY TILL PREVIOUS LINE --------
"""

# ================= COMMON PART (same in all 10 programs) =================
import csv

DOMAIN   = "TrustMesh: Blockchain-Enabled Trusted IoT Framework"   # change per chit
CSV_FILE = "events_7.csv"                                                  # change per chit

with open(CSV_FILE) as f:
    rows = list(csv.DictReader(f))       # rows = list of dicts, one dict per CSV row

print("=== Lamport Logical Clock | " + DOMAIN + " ===")
print(f"Loaded {len(rows)} rows from {CSV_FILE}\n")
# ================= ONLY THE PART BELOW CHANGES =================
from collections import defaultdict

clock, pending, log = {}, defaultdict(list), []

for r in rows:
    p, kind, eid = r["process_id"], r["event_type"].upper(), r["event_id"]
    if p not in clock:
        clock[p] = int(r["initial_clock"])
    old = clock[p]
    if kind == "SEND":
        clock[p] += 1
        pending[r["message_to"]].append((p, clock[p]))
        print(f"{eid} {p} SEND -> {r['message_to']}: L = {old}+1 = {clock[p]}")
    elif kind == "RECEIVE":
        sender, t_msg = pending[p].pop(0) if pending[p] else ("-", 0)
        clock[p] = max(old, t_msg) + 1
        print(f"{eid} {p} RECEIVE from {sender}: L = max({old},{t_msg})+1 = {clock[p]}")
    else:
        clock[p] += 1
        print(f"{eid} {p} LOCAL: L = {old}+1 = {clock[p]}")
    log.append((clock[p], p, eid, kind))

log.sort()                       # (timestamp, process_id) = total order
print("\n=== TOTAL CAUSAL ORDER ===")
for i, (ts, p, eid, kind) in enumerate(log, 1):
    print(f"{i}. {eid:4} (L={ts}) on {p} [{kind}]")
