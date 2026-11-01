"""
RMI / RPC - Remote Invocation & Procedure Dispatch Simulation

HOW TO RUN IN EXAM:
 1. Open Notepad, copy ONLY the CSV lines below (between the two markers).
 2. File > Save As > Save as type: "All Files" > name: rpc_calls_1.csv
    (save in the SAME folder as this .py file)
 3. In VS Code terminal run:  python RMI_RPC.py
 4. Change DOMAIN and CSV_FILE below to match your chit.

CSV FILE NAME: rpc_calls_1.csv
------------ COPY FROM NEXT LINE ------------
call_id,client_name,method_name,param_value,timestamp
101,Client_A,processData,450,10:00:01
102,Client_B,squareValue,12,10:00:03
103,Client_A,validateTransaction,50,10:00:05
104,Client_C,computeHash,999,10:00:07
105,Client_B,unknownMethod,5,10:00:09
------------ COPY TILL PREVIOUS LINE --------
"""

# ================= COMMON PART (same in all 10 programs) =================
import csv

DOMAIN   = "TrustMesh: Blockchain-Enabled Trusted IoT Framework"   # change per chit
CSV_FILE = "rpc_calls_1.csv"                                                  # change per chit

with open(CSV_FILE) as f:
    rows = list(csv.DictReader(f))       # rows = list of dicts, one dict per CSV row

print("=== RMI / RPC Simulation | " + DOMAIN + " ===")
print(f"Loaded {len(rows)} rows from {CSV_FILE}\n")
# ================= ONLY THE PART BELOW CHANGES =================
import json

def processData(x):          return x * 2
def squareValue(x):          return x * x
def validateTransaction(x):  return "VALID" if x >= 100 else "INVALID"
def computeHash(x):          return (x * 31) % 1000
REGISTRY = {"processData": processData, "squareValue": squareValue,
            "validateTransaction": validateTransaction, "computeHash": computeHash}

def server_execute(request):                 # SERVER side
    req = json.loads(request)                # unmarshal
    func = REGISTRY.get(req["method"])
    if func is None:
        return json.dumps({"error": "Method not found on server"})
    print(f"[SERVER EXECUTION] Processing {req['args'][0]} using {req['method']}()")
    return json.dumps({"result": func(*req["args"])})

for row in rows:                             # CLIENT side
    request = json.dumps({"method": row["method_name"], "args": [int(row["param_value"])]})
    print(f"[DISPATCH] {row['client_name']} invoking {row['method_name']}({row['param_value']}) | call_id={row['call_id']}")
    print(f"           Marshalled -> {request}")
    response = json.loads(server_execute(request))
    if "error" in response:
        print(f"[RETURN] ERROR: {response['error']}\n")
    else:
        print(f"[RETURN] Result for call {row['call_id']} = {response['result']}\n")
