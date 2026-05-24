import csv
import random
import time
import os
from datetime import datetime

output_dir = "./logs/"


users = [
    "USER1001",
    "USER1002",
    "USER1003",
    "",
    None
]

devices = [
    "Android",
    "iPhone",
    "Tablet",
    "",
    None
]

events = [
    "LOGIN",
    "LOGOUT",
    "PURCHASE",
    "APP_OPEN",
    "APP_CRASH",
    "API_ERROR",
    None
]

locations = [
    "YEMEN",
    "EGYPT",
    "SAUDI_ARABIA",
    "QATAR",
    "",
    None
]

def random_timestamp():

    formats = [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        datetime.now().strftime("%d/%m/%Y %H:%M"),
        datetime.now().strftime("%m-%d-%Y"),
        "INVALID_TIMESTAMP"
    ]

    return random.choice(formats)

def generate_log():

    log_id = random.randint(100000, 999999)

    user_id = random.choice(users)

    device = random.choice(devices)

    event = random.choice(events)

    session_duration = random.choice([
        random.randint(1, 5000),
        "",
        -50,
        "INVALID"
    ])

    app_version = random.choice([
        "1.0.0",
        "1.2.1",
        "2.0.0",
        "",
        None
    ])

    location = random.choice(locations)

    timestamp = random_timestamp()

    return [
        log_id,
        user_id,
        device,
        event,
        session_duration,
        app_version,
        location,
        timestamp
    ]

while True:

    filename = f"{output_dir}/mobile_logs_{int(time.time())}.csv"

    with open(filename, "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            "log_id",
            "user_id",
            "device_type",
            "event_type",
            "session_duration",
            "app_version",
            "location",
            "event_time"
        ])

        for i in range(1000):

            record = generate_log()

            # duplicate records
            if random.random() < 0.1:
                writer.writerow(record)

            corrupted rows
            if random.random() < 0.05:
                file.write("CORRUPTED_ROW_DATA\n")
                continue

            missing columns
            if random.random() < 0.05:
                file.write("1001,USER1001\n")
                continue

            writer.writerow(record)

    print(f"Generated: {filename}")

    time.sleep(5)