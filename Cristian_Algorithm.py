"""
Cristian's Algorithm - Physical Clock Sync & RTT Compensation

HOW TO RUN IN EXAM:
 1. Open Notepad, copy ONLY the CSV lines below (between the two markers).
 2. File > Save As > Save as type: "All Files" > name: cristian_clocks_8.csv
    (save in the SAME folder as this .py file)
 3. In VS Code terminal run:  python Cristian_Algorithm.py
 4. Change DOMAIN and CSV_FILE below to match your chit.

CSV FILE NAME: cristian_clocks_8.csv
------------ COPY FROM NEXT LINE ------------
client_id,t0_send_ms,t_server_ms,t1_recv_ms
C1,1000,1050,1100
C2,2000,2300,2060
C3,3000,3040,3020
C4,4000,3900,4200
------------ COPY TILL PREVIOUS LINE --------
"""

# ================= COMMON PART (same in all 10 programs) =================
import csv

DOMAIN   = "TrustMesh: Blockchain-Enabled Trusted IoT Framework"   # change per chit
CSV_FILE = "cristian_clocks_8.csv"                                                  # change per chit

with open(CSV_FILE) as f:
    rows = list(csv.DictReader(f))       # rows = list of dicts, one dict per CSV row

print("=== Cristian's Algorithm | " + DOMAIN + " ===")
print(f"Loaded {len(rows)} rows from {CSV_FILE}\n")
# ================= ONLY THE PART BELOW CHANGES =================
for r in rows:
    t0, ts, t1 = int(r["t0_send_ms"]), int(r["t_server_ms"]), int(r["t1_recv_ms"])
    rtt        = t1 - t0
    est_server = ts + rtt / 2
    offset     = est_server - t1
    print(f"Client {r['client_id']}:")
    print(f"  RTT                   = {t1} - {t0} = {rtt} ms")
    print(f"  Estimated server time = {ts} + {rtt}/2 = {est_server} ms")
    print(f"  Offset (drift)        = {est_server} - {t1} = {offset:+} ms")
    print(f"  Adjusted client time  = {t1 + offset} ms  (accuracy +/- {rtt/2} ms)\n")
