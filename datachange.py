import csv
import json
import os


DATABASE_FILE = str(os.getcwd()) + "/gagnasafn.csv"

with open(DATABASE_FILE, encoding='utf-8') as f:
    database = csv.DictReader(f)
    rows = list(database)

with open('data.json', mode='w+', encoding='utf-8') as f:
    dump = json.dumps(rows, ensure_ascii=False)
    f.writelines(dump)

