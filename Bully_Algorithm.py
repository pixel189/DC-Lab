"""
Bully Algorithm - Leader Election & Coordinator Failure Recovery

HOW TO RUN IN EXAM:
 1. Open Notepad, copy ONLY the CSV lines below (between the two markers).
 2. File > Save As > Save as type: "All Files" > name: bully_cluster_2.csv
    (save in the SAME folder as this .py file)
 3. In VS Code terminal run:  python Bully_Algorithm.py
 4. Change DOMAIN and CSV_FILE below to match your chit.

CSV FILE NAME: bully_cluster_2.csv
------------ COPY FROM NEXT LINE ------------
node_id,is_alive,is_current_coordinator
1,TRUE,FALSE
2,TRUE,FALSE
3,TRUE,FALSE
4,TRUE,FALSE
5,FALSE,FALSE
6,FALSE,TRUE
------------ COPY TILL PREVIOUS LINE --------
"""

# ================= COMMON PART (same in all 10 programs) =================
import csv

DOMAIN   = "TrustMesh: Blockchain-Enabled Trusted IoT Framework"   # change per chit
CSV_FILE = "bully_cluster_2.csv"                                                  # change per chit

with open(CSV_FILE) as f:
    rows = list(csv.DictReader(f))       # rows = list of dicts, one dict per CSV row

print("=== Bully Election Algorithm | " + DOMAIN + " ===")
print(f"Loaded {len(rows)} rows from {CSV_FILE}\n")
# ================= ONLY THE PART BELOW CHANGES =================
alive = {int(r["node_id"]): r["is_alive"].strip().upper() == "TRUE" for r in rows}
coordinator = next(int(r["node_id"]) for r in rows if r["is_current_coordinator"].strip().upper() == "TRUE")

print(f"[DETECT] Coordinator = Node {coordinator}, alive = {alive[coordinator]}")
if alive[coordinator]:
    print("Coordinator is healthy. No election."); raise SystemExit
print(f"[FAILURE] Coordinator Node {coordinator} not responding!\n")

held = set()

def election(n):
    if n in held: return
    held.add(n)
    higher = [x for x in sorted(alive) if x > n]
    print(f"[ELECTION] Node {n} sends ELECTION to higher nodes {higher}")
    responders = []
    for h in higher:
        if alive[h]:
            print(f"   Node {n} -> Node {h}: ELECTION")
            print(f"   Node {h} -> Node {n}: OK  (Node {h} bullies Node {n})")
            responders.append(h)
        else:
            print(f"   Node {n} -> Node {h}: ELECTION ... no reply (Node {h} is DOWN)")
    if not responders:
        print(f"\n[WINNER] Node {n} is the highest alive node")
        for x in sorted(alive):
            if x != n and alive[x]:
                print(f"   Node {n} -> Node {x}: COORDINATOR({n})")
        print(f"[COORDINATOR] Node {n} is the NEW LEADER")
    else:
        for h in responders:
            election(h)

initiator = min(n for n in alive if alive[n])
print(f"[INITIATOR] Node {initiator}\n")
election(initiator)
