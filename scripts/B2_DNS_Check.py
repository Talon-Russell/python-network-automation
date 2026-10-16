import csv
import telnetlib
import time
#lists known good DNS and malicious dns
GOOD_DNS_1 = "10.10.10.10"
GOOD_DNS_2 = "10.10.10.20"
BAD_DNS = "203.0.113.10"
#opens csv
with open("network_devices.csv", "r") as csv_file:
    devices = csv.DictReader(csv_file)
#reads name, port, and OS of devices
    for device in devices:
        name = device["Device Name"]
        port = int(device["Access Port"])
        os_type = device["OS"]
        print()
        print("ANALYZING " + name + "...")
#displays all SMTP as connected per gns3
        if name == "SMTP":
            print(name + " - CONNECTED")
            continue
#Create telnets session into Ubuntu devices 
        try:
            tn = telnetlib.Telnet("localhost", port, timeout=5)
            if os_type == "Ubuntu":
                username = device["Username"]
                password = device["Password"]
                tn.read_until(b"login:", timeout=5)
                tn.write(username.encode() + b"\n")
                tn.read_until(b"Password:", timeout=5)
                tn.write(password.encode() + b"\n")
                time.sleep(1)
                tn.write(b"resolvectl status\n")
                time.sleep(2)
                output = tn.read_very_eager().decode(errors="ignore")
               #scans telnet for DNS Server info
                dns_line = ""
                for line in output.split("\n"):
                    if "DNS Servers" in line:
                        dns_line = line
#checks dns and prints good or bad
                if BAD_DNS in dns_line:
                    print(name + " - MALICIOUS DNS DETECTED")
                elif GOOD_DNS_1 in dns_line or GOOD_DNS_2 in dns_line:
                    print(name + " - KNOWN GOOD DNS")
                else:
                    print(name + " - MALICIOUS DNS DETECTED")
#logs into switches
            elif os_type == "VyOS":
                username = device["Username"]
                password = device["Password"]
                tn.read_until(b"login:", timeout=5)
                tn.write(username.encode() + b"\n")
                tn.read_until(b"Password:", timeout=5)
                tn.write(password.encode() + b"\n")
                time.sleep(1)
                print(name + " - CONNECTED")
            else:
                print(name + " - CONNECTED")
            tn.close()
        except Exception:
            print(name + " - FAILED TO CONNECT")