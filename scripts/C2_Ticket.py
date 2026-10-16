import csv
import requests

API_URL = "http://api.d522.wgu.internal:5000/api/tickets"  # ticket website
API_TOKEN = "Bearer vGkbXkGLqQSo7YLflp9DutuG8st4xdPPF7wnTcwB0FE"   # authentication code
CSV_FILENAME = "network_devices.csv"
TARGET_DEVICES = ["PC2", "PC3", "SVR1", "SVR2"]  # affected devices


def get_headers():
    return {
        "Authorization": API_TOKEN,
        "Content-Type": "application/json"
    }


# ticket details
def build_ticket(device_name):
    return {
        "assigned_to": "Network Team",
        "description": f"DNS compromise detected on {device_name}.",
        "priority": "low",
        "requester_email": "monitor@d522.wgu.internal",
        "status": "open",
        "title": f"DNS Compromised - {device_name}"
    }


def load_target_devices(filename, targets):
    with open(filename, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader if row["Device Name"] in targets]


# submits ticket
def submit_ticket(session, device_name):
    ticket = build_ticket(device_name)
    response = session.post(API_URL, json=ticket)
    print("--------------------------------")
    print("Device:", device_name)
    print("Status Code:", response.status_code)
    print("Response:")
    print(response.text)
    return response


def main():
    devices = load_target_devices(CSV_FILENAME, TARGET_DEVICES)

    if not devices:
        print("Check TARGET_DEVICES and 'Device Name' column.")
        return

    session = requests.Session()
    session.headers.update(get_headers())

    for row in devices:
        submit_ticket(session, row["Device Name"])

    print("Ticket Submitted")


if __name__ == "__main__":
    main()