"""
PLAY WITH CSV


"""

import csv

fuckin_data = [
    {"date": "2021/06/15","performer": "washizaki","start": "06:00","close": "06:30",},
    {"date": "2021/06/15","performer": "washizaki","start": "06:00","close": "06:30",},
    {"date": "2021/06/15","performer": "washizaki","start": "06:00","close": "06:30",},
    {"date": "2021/06/15","performer": "washizaki","start": "06:00","close": "06:30",},
    {"date": "2021/06/15","performer": "washizaki","start": "06:00","close": "06:30",},
    {"date": "2021/06/15","performer": "washizaki","start": "06:00","close": "06:30",},
    ]

def main():
    with open("playground/out/fckncsv.csv", "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["date", "performer", "start", "close"])
        writer.writeheader()
        for dict in fuckin_data:
            writer.writerow(dict)

main()


def writeRowByRow(data: dict):
    with open("playground/out/fckncsv.csv", "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["date", "performer", "start", "close"])
        writer.writeheader()
        for dict in fuckin_data:
            writer.writerow(dict)


