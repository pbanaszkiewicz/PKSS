import csv
import json

filename = 'ex1_ver2'  # no extension!

# read data in
with open('{}.txt'.format(filename), 'r') as f:
    lines = f.readlines()

# translate from JSON to Python
data = [json.loads(line) for line in lines]

with open('{}.csv'.format(filename), 'w') as f:
    # you can specify yourself, for example: ['time', 't_zcb']
    columns = list(data[0].keys()) 
    writer = csv.DictWriter(f, fieldnames=columns)

    writer.writeheader()

    for line in data:
        writer.writerow(line)
