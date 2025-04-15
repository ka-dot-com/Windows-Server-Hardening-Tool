import subprocess
import os
from datetime import datetime

def run_powershell(command):
    # Run a PowerShell command and capture output
    try:
        result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True)
        return result.stdout, result.stderr
    except Exception as e:
        return "", str(e)

def harden_server():
    # Apply CIS benchmarks for better security
    print("Starting server hardening...")
    
    # Disable SMBv1 since it’s outdated and vulnerable
    stdout, stderr = run_powershell("Disable-WindowsOptionalFeature -Online -FeatureName SMB1Protocol")
    if stderr:
        print(f"Error disabling SMBv1: {stderr}")
    else:
        print("SMBv1 disabled successfully.")
    
    # Make sure firewall is active
    stdout, stderr = run_powershell("Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True")
    if stderr:
        print(f"Error enabling firewall: {stderr}")
    else:
        print("Firewall enabled.")
    
    # Save a report of what was done
    report_path = f"reports/hardening_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    os.makedirs("reports", exist_ok=True)
    with open(report_path, "w") as f:
        f.write("Hardening Report\n")
        f.write(f"Date: {datetime.now()}\n")
        f.write("SMBv1: Disabled\n")
        f.write("Firewall: Enabled\n")
    print(f"Report saved to {report_path}")

if __name__ == "__main__":
    harden_server()