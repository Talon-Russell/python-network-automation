import csv
with open("network_devices.csv", "r") as files:
    devices = csv.reader(files) 
    next(devices)
    print("Network Device Names")
    for device in devices:
        print(device[1])
#opens CSV and reads first column
