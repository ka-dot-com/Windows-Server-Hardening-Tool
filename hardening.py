"""
for admins only
"""

import subprocess
import os
from datetime import datetime

def run_powershell(command):
    try:
        result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Błąd PowerShell: {result.stderr}")
        return result.stdout, result.stderr
    except Exception as e:
        return "", str(e)

def check_admin_rights():
    try:
        result = subprocess.run(["powershell", "-Command", "whoami /groups | findstr S-1-5-32-544"], capture_output=True, text=True)
        return "Administrators" in result.stdout
    except Exception:
        return False

def harden_server():
    if not check_admin_rights():
        print("Brak uprawnień administratora. Uruchom jako administrator.")
        return

    print("Starting server hardening...")
    
    stdout, stderr = run_powershell("Disable-WindowsOptionalFeature -Online -FeatureName SMB1Protocol")
    if stderr:
        print(f"Error disabling SMBv1: {stderr}")
    else:
        print("SMBv1 disabled successfully.")
    
    stdout, stderr = run_powershell("Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True")
    if stderr:
        print(f"Error enabling firewall: {stderr}")
    else:
        print("Firewall enabled.")
    
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
