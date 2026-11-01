"""
Berkeley's Algorithm - Clock Averaging & Fault-Tolerant Offset Adjustment

HOW TO RUN IN EXAM:
 1. Open Notepad, copy ONLY the CSV lines below (between the two markers).
 2. File > Save As > Save as type: "All Files" > name: node_clocks_3.csv
    (save in the SAME folder as this .py file)
 3. In VS Code terminal run:  python Berkeley_Algorithm.py
 4. Change DOMAIN and CSV_FILE below to match your chit.

CSV FILE NAME: node_clocks_3.csv
------------ COPY FROM NEXT LINE ------------
node_id,clock_time_sec,is_faulty
N1,3600,FALSE
N2,3610,FALSE
N3,3590,FALSE
N4,3625,FALSE
N5,9999,TRUE
------------ COPY TILL PREVIOUS LINE --------
"""

# ================= COMMON PART (same in all 10 programs) =================
import csv

DOMAIN   = "TrustMesh: Blockchain-Enabled Trusted IoT Framework"   # change per chit
CSV_FILE = "node_clocks_3.csv"                                                  # change per chit

with open(CSV_FILE) as f:
    rows = list(csv.DictReader(f))       # rows = list of dicts, one dict per CSV row

print("=== Berkeley's Algorithm | " + DOMAIN + " ===")
print(f"Loaded {len(rows)} rows from {CSV_FILE}\n")
# ================= ONLY THE PART BELOW CHANGES =================
THRESHOLD = 300      # seconds

nodes = {r["node_id"]: (int(r["clock_time_sec"]), r["is_faulty"].strip().upper() == "TRUE") for r in rows}

print("Step 1: Master polls all nodes")
for n, (t, bad) in nodes.items():
    print(f"  {n}: {t} sec {'(flagged faulty)' if bad else ''}")

times  = sorted(t for t, _ in nodes.values())
median = times[len(times) // 2]

print("\nStep 2: Discard faulty / outlier clocks")
valid = {}
for n, (t, bad) in nodes.items():
    if bad or abs(t - median) > THRESHOLD:
        print(f"  DISCARDED {n} ({t} sec)")
    else:
        valid[n] = t

avg = sum(valid.values()) / len(valid)
print(f"\nStep 3: Average of {list(valid.values())} = {avg:.2f} sec")

print("\nStep 4: Adjustment sent to each node")
for n, (t, _) in nodes.items():
    print(f"  {n}: {t} -> {avg:.2f}   adjustment = {avg - t:+.2f} sec")
