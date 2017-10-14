'''
This file converts the json file to the format of simple search.
It makes sure words in document is such that 200 <= words <= 2000.
It also culls documents with similar repeated content.
'''

### Imports

import os
import json
import pprint

### Document requirements

MIN_WORD_LENGTH = 200
MAX_WORD_LENGTH = 2000
COLLECTION_SIZE = 30

### Methods

def open_json_file(filename):
    if os.path.exists(filename):
        print("File " + filename + " found")
        with open(filename, 'r') as json_data:
            data = json_data.read()
            json_data.close()
            data = data[1:len(data) - 2]
            items = data.split('},')
            new_data = [] # the extract json objects
            seen = {}
            for i in range(0, len(items)):
                items[i] = items[i].rstrip()
                # Add missing brace after split to make proper json object
                if items[i][len(items[i]) - 1] != "}":
                    items[i] += "}"

                j_data = json.loads(items[i])

                content = j_data["content"]
                id = j_data['id']
                if content in seen or content == "":
                    continue
                else:
                    seen[content] = id

                word_count = len(content.split())
                if word_count < 200 or word_count > 2000:
                    continue
                else:
                    new_data.append(j_data)
            for n in new_data:
                print (n)
            print(len(new_data))


    else:
        print("Could not find "+filename)

open_json_file("extracted.json")

