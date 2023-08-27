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
import fileinput

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
SELECT  f.code_before, f.code_after, cw.extended_description
FROM file_change f, commits c, fixes fx, cve cv, cwe_classification cc, cwe cw
WHERE f.hash = c.hash 
AND c.hash = fx.hash 
AND fx.cve_id = cv.cve_id 
AND cv.cve_id = cc.cve_id
AND cw.cwe_id = cc.cwe_id
AND f.code_before != "None"
AND f.code_after != "None"
"""
query2 = """
SELECT * FROM file_change f
"""
code_fixes = pd.read_sql_query(query, conn)
print(code_fixes.columns)

json_entries = []

count = 0
for index, row in code_fixes.iterrows():
    if len(row['code_before']) < 4000 and len(row['code_after']) < 1000 and len(row['extended_description']) > 5 and "Insufficient Information" not in row['extended_description']:
        count += 1
        entry = {"messages": [{"role": "system", "content": "Provide new code to fix the vulnerabilities in the code given."},{"role": "user", "content": row['code_before']},{"role": "assistant", "content": row['extended_description'] + "Here is the fixed code: " + row['code_after']}]}
        json_entries.append(entry)
    if count > 1099:
        break

print(count)
def prepare_data(dictionary_data, final_file_name):
    
    with open(final_file_name, 'w') as outfile:
        for entry in dictionary_data:
            json.dump(entry, outfile)
            outfile.write('\n')       

# Write the JSON entries to a file
prepare_data(json_entries[:1000], "output_temp.jsonl")
prepare_data(json_entries[1000:], "validation_temp.jsonl")


def process_content(content):
    # Replace unicode escape sequences with their corresponding characters
    content = content.replace("\\n", "").replace("\\t", "")
    content = content.replace("\n", "").replace("\t", "")
    return content

# Read the JSONL file and fix the content
with open("output_temp.jsonl", "r") as input_file, open("output.jsonl", "w") as output_file:
    for line in input_file:
        data = json.loads(line)
        messages = data["messages"]
        
        for message in messages:
            message["content"] = process_content(message["content"])
        
        # Write the updated JSON structure back to the output file
        json.dump(data, output_file)
        output_file.write("\n")

with open("validation_temp.jsonl", "r") as input_file, open("validation.jsonl", "w") as output_file:
    for line in input_file:
        data = json.loads(line)
        messages = data["messages"]
        
        for message in messages:
            message["content"] = process_content(message["content"])
        
        # Write the updated JSON structure back to the output file
        json.dump(data, output_file)
        output_file.write("\n")







