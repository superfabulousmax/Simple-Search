'''
Runs query.1, query.2 and query.3
Writes results to textfile in trec format
'''

import query
import parameters
import os

OUT_DIR = "testbed/"
RESULT_FILE = "control_results.txt"
if parameters.use_thesaurus:
    RESULT_FILE = "thesaurus_results.txt"
QUERY_DIR = "testbed/"
COLLECTION = "testbed/emotions_collection"

# clear results textfile
output = OUT_DIR + RESULT_FILE
if os.path.isfile(OUT_DIR + RESULT_FILE):
    with open(output, "w") as f:
        f.write("")
    f.close()

# run queries
for i in range(1, 4):
    f = open(QUERY_DIR + "query." + str(i), "r")
    lines = f.readlines()
    text_query = lines[0]
    if (text_query != ""):
        query.main(str(i), COLLECTION, text_query)
