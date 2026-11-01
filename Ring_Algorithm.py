"""
Ring Algorithm - Leader Election & Token Circulation

HOW TO RUN IN EXAM:
 1. Open Notepad, copy ONLY the CSV lines below (between the two markers).
 2. File > Save As > Save as type: "All Files" > name: ring_nodes_15.csv
    (save in the SAME folder as this .py file)
 3. In VS Code terminal run:  python Ring_Algorithm.py
 4. Change DOMAIN and CSV_FILE below to match your chit.

CSV FILE NAME: ring_nodes_15.csv
------------ COPY FROM NEXT LINE ------------
node_id,next_node_id,is_active,priority_rank
1,2,TRUE,85
2,3,TRUE,70
3,4,FALSE,60
4,5,TRUE,90
5,6,TRUE,75
6,1,FALSE,95
------------ COPY TILL PREVIOUS LINE --------
"""

# ================= COMMON PART (same in all 10 programs) =================
import csv

DOMAIN   = "TrustMesh: Blockchain-Enabled Trusted IoT Framework"   # change per chit
CSV_FILE = "ring_nodes_15.csv"                                                  # change per chit

with open(CSV_FILE) as f:
    rows = list(csv.DictReader(f))       # rows = list of dicts, one dict per CSV row

print("=== Ring Election Algorithm | " + DOMAIN + " ===")
print(f"Loaded {len(rows)} rows from {CSV_FILE}\n")
# ================= ONLY THE PART BELOW CHANGES =================
nodes = {int(r["node_id"]): {"next": int(r["next_node_id"]),
                             "active": r["is_active"].strip().upper() == "TRUE",
                             "rank": int(r["priority_rank"])} for r in rows}

coordinator = max(nodes)                       # old coordinator = highest ID
if nodes[coordinator]["active"]:
    print(f"Coordinator {coordinator} is alive. No election needed."); raise SystemExit
print(f"[FAILURE] Coordinator Node {coordinator} is DOWN!")

initiator = next((n for n, d in nodes.items() if d["next"] == coordinator and d["active"]),
                 min(n for n in nodes if nodes[n]["active"]))
print(f"[INITIATOR] Node {initiator} starts the election\n")

token, current = [initiator], initiator
while True:
    nxt = nodes[current]["next"]
    while not nodes[nxt]["active"]:
        print(f"   Node {nxt} is DOWN, skipping")
        nxt = nodes[nxt]["next"]
    print(f"[TOKEN] ELECTION{token} : Node {current} -> Node {nxt}")
    if nxt == initiator:
        break
    token.append(nxt)
    current = nxt

winner = max(token)
print(f"\n[ELECTED] Node {winner} (priority_rank={nodes[winner]['rank']}) is the NEW COORDINATOR")
print("\n[COORDINATOR MESSAGE] circulating:")
current = winner
for _ in token:
    nxt = nodes[current]["next"]
    while not nodes[nxt]["active"]:
        nxt = nodes[nxt]["next"]
    print(f"   Node {current} -> Node {nxt} : COORDINATOR({winner})")
    current = nxt
