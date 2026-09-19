import time
from datetime import datetime
from pymodbus.client import ModbusTcpClient
import openpyxl
import os

# ==========================================
# PLC Configuration Settings
# ==========================================
PLC_IP = "192.168.1.5"    # Delta DVP-50MC IP Address
PLC_PORT = 502
SLAVE_ID = 1

# ==========================================
# Excel Output File Settings
# ==========================================
EXCEL_FILE = "Production_Log_RealTime.xlsx"

def init_excel():
    """Initialize Excel log file with headers if missing."""
    if not os.path.exists(EXCEL_FILE):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Production_Log"
        headers = [
            "Timestamp", "Shift", "Total Production", "Target", 
            "OK Count", "Rework Count", "Rejection Count", 
            "Defect Code", "Defect Description", "Achievement %"
        ]
        ws.append(headers)
        wb.save(EXCEL_FILE)
        print(f"✅ Excel log file '{EXCEL_FILE}' initialized successfully.")

def get_defect_description(code):
    """Map numerical defect code to human-readable description."""
    defects = {
        0: "None / Good Quality",
        1: "Dimension Out of Spec",
        2: "Surface Scratch / Visual Defect",
        3: "Weight Mismatch",
        4: "Assembly Alignment Fault"
    }
    return defects.get(code, f"Unknown Defect ({code})")

def get_current_shift():
    """Determine manufacturing shift based on system time."""
    now = datetime.now().time()
    if time(6, 0) <= now < time(14, 0):
        return "Shift A"
    elif time(14, 0) <= now < time(22, 0):
        return "Shift B"
    else:
        return "Shift C"

def read_plc_and_log():
    """Poll PLC registers over Modbus TCP and log into Excel continuously."""
    client = ModbusTcpClient(PLC_IP, port=PLC_PORT)
    
    if not client.connect():
        print(f"❌ Connection Error: Unable to connect to PLC at {PLC_IP}:{PLC_PORT}")
        return

    print(f"✅ Connected to Delta DVP-50MC PLC at {PLC_IP}:{PLC_PORT}")

    init_excel()

    wb = openpyxl.load_workbook(EXCEL_FILE)
    ws = wb["Production_Log"]

    try:
        while True:
            # Read 13 registers starting from address 100 (D100 to D112)
            result = client.read_holding_registers(address=100, count=13, slave=SLAVE_ID)

            if not result.isError():
                regs = result.registers
                total_prod   = regs[0]   # D100
                target_prod  = regs[2]   # D102
                ok_count     = regs[4]   # D104
                rework_count = regs[6]   # D106
                reject_count = regs[8]   # D108
                defect_code  = regs[10]  # D110
                achievement  = regs[12]  # D112

                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                shift = get_current_shift()
                defect_desc = get_defect_description(defect_code)

                # Append data row
                row = [
                    timestamp, shift, total_prod, target_prod,
                    ok_count, rework_count, reject_count,
                    defect_code, defect_desc, f"{achievement}%"
                ]
                ws.append(row)
                wb.save(EXCEL_FILE)

                print(f"[{timestamp}] {shift} | Total: {total_prod} | OK: {ok_count} | Rework: {rework_count} | Reject: {reject_count} | Defect: {defect_desc} | Achievement: {achievement}%")
            else:
                print("⚠️ Communication Warning: Error reading PLC registers.")

            time.sleep(5)  # Polling interval (5 seconds)

    except KeyboardInterrupt:
        print("\n🛑 Logging session stopped by user.")
    finally:
        client.close()

if __name__ == "__main__":
    read_plc_and_log()
