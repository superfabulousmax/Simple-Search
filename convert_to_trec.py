'''
Converts relevance judgements to trec format
'''

import os

# Trec relevance format:
# <query-id> <literal '0'> <document-id> <document relevance>

REL_DIR = "testbed/"
output = REL_DIR+"trec_relevance_judgements.txt"

# clear judgements textfile
if os.path.isfile(output):
    with open(output, "w") as f:
        f.write("")
    f.close()

# write judgements to one file in trec format
for q in range(1, 4):
    if os.path.isfile(REL_DIR + "relevance." + str(q)):
        f = open(REL_DIR + "relevance." + str(q), "r")
        lines = f.readlines()
        f.close()
        with open(output, "a") as f:
            doc_id = 1
            for rel in lines:
                # <query-id> <literal '0'> <document-id> <document relevance>
                f.write(str(q) + " 0 " + str(doc_id) + " " + str(rel))
                doc_id += 1
            f.write("\n")
        f.close()
    else:
        print("Could not open file: " + REL_DIR + "relevance." + str(q))