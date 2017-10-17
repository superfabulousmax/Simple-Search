'''
This file converts the json file to the format of simple search.
It makes sure words in document is such that 200 <= words <= 2000.
It also culls documents with similar repeated content.
'''

### Imports

import os
import json
### Document requirements

MIN_WORD_LENGTH = 200
MAX_WORD_LENGTH = 2000
COLLECTION_SIZE = 30
COLLECTION_NAME = "testbed/emotions_collection2"

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
                    new_data.append(items[i])
            for n in new_data:
                print (n)
            print(str(len(new_data))+ " items extracted")
            return new_data

    else:
        print("Could not find "+filename)
        return []

'''
Format: 
.I 1
.T 
one apple
.W 
apple
'''
def write_to_simple_format(data):
    with open(COLLECTION_NAME, "a") as collection_file:
        int_id = 1
        for i in data:
            j_data = json.loads(i)
            content = str(j_data["content"].encode("utf-8")) # there are some Greek letters that need to be encoded before writing to file
            id = j_data["id"]
            title = j_data["title"]

            collection_file.write(".I "+str(int_id)+"\n")
            collection_file.write(".T\n" + title + "\n")
            collection_file.write(".W\n" + content[2:len(content)-1] + "\n") # remove b' and last '
            int_id += 1
        collection_file.write(".I " + str(int_id) + "\n") # the cranfield format seems to expect an extra id at bottom
    collection_file.close()

write_to_simple_format(open_json_file("extracted.json"))

