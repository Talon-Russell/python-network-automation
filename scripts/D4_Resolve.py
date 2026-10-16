
import telnetlib
import time

devices = [
    {"name": "PC2", "port": 5029},
    {"name": "PC3", "port": 5031},
    {"name": "SVR1", "port": 5022},
    {"name": "SVR2", "port": 5014}
]

#resolves dns to known good
DNS_CMD = "sudo resolvectl dns ens3 10.10.10.10 10.10.10.20"


def update_dns(device):
    print(f"Updating DNS on {device['name']}...", end=" ")
    tn = telnetlib.Telnet("localhost", device["port"])
    tn.write(b"\n")
    time.sleep(1)
    screen = tn.read_very_eager().decode()

    if "ubuntu@" not in screen and "login:" in screen:
        tn.write(b"ubuntu\n")
        time.sleep(1)
        tn.write(b"ubuntu\n")
        time.sleep(2)

    tn.write(f"{DNS_CMD}\n".encode())
    time.sleep(2)
    screen = tn.read_very_eager().decode()

    # Only send a password if prompted
    if "Password:" in screen:
        tn.write(b"ubuntu\n")
        time.sleep(2)
        screen += tn.read_very_eager().decode()

    if "Failed to set DNS" in screen or "not found" in screen:
        print("FAILED (resolvectl/systemd-resolved unavailable)")
        tn.write(b"exit\n")
        tn.close()
        return

    tn.write(b"resolvectl status\n")
    time.sleep(2)
    output = tn.read_very_eager().decode()

    #confirms it went through or failed
    if "10.10.10.10" in output and "10.10.10.20" in output:
        print("Success")
    else:
        print("FAILED (verification did not show new DNS servers)")

    tn.write(b"exit\n")
    tn.close()


for device in devices:
    update_dns(device)

print("DNS update complete.")