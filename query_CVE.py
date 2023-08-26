import pandas as pd
import matplotlib.pyplot as plt
import sqlite3 as lite
from sqlite3 import Error
from pathlib import Path
from datetime import date
import numpy as np
import seaborn as sns
import matplotlib.ticker as tick
import requests
import difflib as diff
import re 
import csv
import ast
import json

def create_connection(db_file):
    """
    create a connection to sqlite3 database
    """
    conn = None
    try:
        conn = lite.connect(db_file, timeout=10)  # connection via sqlite3
        # engine = sa.create_engine('sqlite:///' + db_file)  # connection via sqlalchemy
        # conn = engine.connect()
    except Error as e:
        print(e)
    return conn


conn = create_connection("CVEfixes.db")

query = """
SELECT cv.cve_id, f.filename, f.num_lines_added, f.num_lines_deleted, f.code_before, f.code_after, cc.cwe_id 
FROM file_change f, commits c, fixes fx, cve cv, cwe_classification cc
WHERE f.hash = c.hash 
AND c.hash = fx.hash 
AND fx.cve_id = cv.cve_id 
AND cv.cve_id = cc.cve_id 
"""
code_fixes = pd.read_sql_query(query, conn)


json_entries = []

# Iterate through the first 1000 rows of the DataFrame
count = 0
for index, row in code_fixes.iterrows():
    if len(row['code_before']) < 4000 and len(row['code_after']) < 1000:
        count += 1
        entry = {
            "messages": [
                {"role": "system", "content": "Provide new code to fix the vulnerabilities in the code given."},
                {"role": "user", "content": row['code_before']},
                {"role": "assistant", "content": row['code_after']}
            ]
        }
        json_string = json.dumps(entry, indent=2)
        json_entries.append(json_string)
    if count > 999:
        break


# Write the JSON entries to a file
with open("output.json", "w") as f:
    for entry in json_entries:
        f.write(entry + "\n")

print(count)







