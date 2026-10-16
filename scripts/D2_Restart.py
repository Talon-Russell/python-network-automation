import telnetlib
import time

SERVICE = "named"
LOGIN = "ubuntu"

servers = [
    {"label": "DNS1", "port": 5013},
    {"label": "DNS2", "port": 5017}
]

for server in servers:
    print(f"Restarting {server['label']}")

    conn = telnetlib.Telnet("localhost", server["port"])
    conn.write(b"\n")
    time.sleep(1)

    banner = conn.read_very_eager().decode()
    if f"{LOGIN}@" not in banner:
        conn.write(f"{LOGIN}\n".encode())
        time.sleep(1)
        conn.write(f"{LOGIN}\n".encode())
        time.sleep(2)
#command that restarts the servers
    print("\nRunning:")
    print(f"sudo systemctl start {SERVICE}")
    conn.write(f"sudo systemctl start {SERVICE}\n".encode())
    time.sleep(2)
    conn.write(f"{LOGIN}\n".encode())
    time.sleep(2)

    print("\nVerification:")
    print(f"systemctl is-active {SERVICE}")
    conn.write(f"systemctl is-active {SERVICE}\n".encode())
    time.sleep(2)
    result = conn.read_very_eager().decode()

    if "inactive" in result:
        state = "inactive"
    elif "active" in result:
        state = "active"
    else:
        state = "unknown"

    print("\nResult:")
    print(state)

    if state == "active":
        print(f"\n{server['label']} - DNS service is NOW RUNNING")
    elif state == "inactive":
        print(f"\n{server['label']} - DNS service is STILL DOWN")
    else:
        print(f"\n{server['label']} - Unable to determine status")
        print(result)

    conn.write(b"exit\n")
    conn.close()

print("Restart complete.")