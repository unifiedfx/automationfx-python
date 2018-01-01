import csv
from automationfx import *

data = sqlQuery("SELECT name,description FROM device")
all_keys = set().union(*(d.keys() for d in data))
# sorted_keys = sorted(list(set(all_keys)))

with open('device_summary.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f,fieldnames=all_keys)
    writer.writeheader()
    writer.writerows(data)
