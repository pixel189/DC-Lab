"""
MPI Matrix Multiplication - Row Partitioning / Scatter-Gather Simulation

HOW TO RUN IN EXAM:
 1. Open Notepad, copy ONLY the CSV lines below (between the two markers).
 2. File > Save As > Save as type: "All Files" > name: matrix_22.csv
    (save in the SAME folder as this .py file)
 3. In VS Code terminal run:  python MPI_Matrix_Multiplication.py
 4. Change DOMAIN and CSV_FILE below to match your chit.

CSV FILE NAME: matrix_22.csv
------------ COPY FROM NEXT LINE ------------
row_id,col_0,col_1,col_2,col_3
R0,2,4,1,5
R1,3,0,2,1
R2,1,1,1,1
R3,4,2,0,3
------------ COPY TILL PREVIOUS LINE --------
"""

# ================= COMMON PART (same in all 10 programs) =================
import csv

DOMAIN   = "TrustMesh: Blockchain-Enabled Trusted IoT Framework"   # change per chit
CSV_FILE = "matrix_22.csv"                                                  # change per chit

with open(CSV_FILE) as f:
    rows = list(csv.DictReader(f))       # rows = list of dicts, one dict per CSV row

print("=== MPI Matrix Multiplication (Scatter-Gather) | " + DOMAIN + " ===")
print(f"Loaded {len(rows)} rows from {CSV_FILE}\n")
# ================= ONLY THE PART BELOW CHANGES =================
from multiprocessing.dummy import Pool    # worker "processes" simulated with threads

NUM_WORKERS = 3
B = [[1, 2, 0],      # matrix B (4x3), broadcast to all workers
     [0, 1, 3],
     [2, 0, 1],
     [1, 1, 1]]

A = [(r["row_id"], [int(r[c]) for c in ("col_0", "col_1", "col_2", "col_3")]) for r in rows]

def worker(task):
    rank, row_id, row = task
    result = [sum(row[k] * B[k][j] for k in range(len(row))) for j in range(len(B[0]))]
    print(f"[WORKER {rank}] got {row_id}={row} -> dot products = {result}")
    return (row_id, result)

print("[MASTER] Broadcasting matrix B:", B)
print(f"[MASTER] SCATTER: {len(A)} rows -> {NUM_WORKERS} workers")
tasks = [(i % NUM_WORKERS, rid, row) for i, (rid, row) in enumerate(A)]
for rank, rid, row in tasks:
    print(f"   Master -> Worker {rank}: {rid} = {row}")

with Pool(NUM_WORKERS) as pool:
    gathered = pool.map(worker, tasks)

print("\n[MASTER] GATHER complete")
print("=== FINAL PRODUCT MATRIX C = A x B ===")
for rid, row in gathered:
    print(rid, row)
