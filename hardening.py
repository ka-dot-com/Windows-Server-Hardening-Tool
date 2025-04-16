"""
for admins only
"""

import subprocess
import os
import tkinter as tk
from tkinter import messagebox

def check_password_policy():
    try:
        result = subprocess.run(["powershell", "-Command", "Get-ADDefaultDomainPasswordPolicy"], capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"PowerShell Error: {result.stderr}")
        return result.stdout
    except Exception as e:
        return f"Error: {e}"

def harden_server():
    try:
        subprocess.run(["powershell", "-Command", "Disable-WindowsOptionalFeature -Online -FeatureName SMB1Protocol"], check=True)
        subprocess.run(["powershell", "-Command", "Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True"], check=True)
        messagebox.showinfo("Success", "Server hardened successfully!")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to harden server: {e}")

def show_gui():
    root = tk.Tk()
    root.title("Windows Server Hardening Tool")

    tk.Label(root, text="Windows Server Hardening Tool").pack(pady=10)
    tk.Button(root, text="Check Password Policy", command=lambda: messagebox.showinfo("Password Policy", check_password_policy())).pack(pady=5)
    tk.Button(root, text="Harden Server", command=harden_server).pack(pady=5)
    root.mainloop()

if __name__ == "__main__":
    show_gui()
