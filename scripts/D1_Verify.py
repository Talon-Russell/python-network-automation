import telnetlib #used telnet for simplicity

HOST = "localhost"
USERNAME = "ubuntu"
PASSWORD = "ubuntu"
COMMAND = "systemctl is-active named" #command that runs in servers

DEVICES = [
    {"name": "DNS1", "port": 5013},
    {"name": "DNS2", "port": 5017},
]

TIMEOUT = 5 #seconds before it fail out
LOGIN = rb"login:"
PASSWORD_PROMPT = rb"[Pp]assword:"
SHELL_PROMPT = rb"\$\s*$"


def check_device(name, port):
    print(f"Checking {name}")

    try:
        tn = telnetlib.Telnet(HOST, port, timeout=5)
    except OSError as e:
        print(f"\n{name} - Failed to connect: {e}")
        return

    tn.write(b"\n")

    # Waits log in prompt
    index, _, _ = tn.expect([LOGIN, SHELL], TIMEOUT)

    if index == 0:
        # logs into prompt
        tn.write(USERNAME.encode() + b"\n")
        tn.expect([PASSWORD_PROMPT], TIMEOUT)
        tn.write(PASSWORD.encode() + b"\n")
        tn.expect([SHELL_PROMPT], TIMEOUT)
    elif index == -1:
        print(f"\n{name} - Device not responding")
        tn.close()
        return

    tn.write(COMMAND.encode() + b"\n")
    _, _, output = tn.expect([SHELL_PROMPT], TIMEOUT)
    output = output.decode(errors="ignore")

    
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    last_line = lines[-1] if lines else ""

    if "inactive" in output:
        status = "inactive"
    elif "active" in output:
        status = "active"
    else:
        status = "unknown"

    print("\nResult:")
    print(status)
#displays DNS status per server
    if status == "inactive":
        print(f"\n{name} - DNS service is DOWN")
    elif status == "active":
        print(f"\n{name} - DNS service is UP")
    else:
        print(f"\n{name} - Failed to get status")
        print(output)

    tn.write(b"exit\n")
    tn.close()

if__name__=="main__":

for device in DEVICES:
    check_device(device["name"], device["port"])

print("DNS Verification complete.")