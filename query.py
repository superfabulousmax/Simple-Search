# Simple extended boolean search engine: query module
# Hussein Suleman
# 14 April 2016

import re
import math
import sys
import os

import porter

import parameters

import py_thesaurus # to use synonyms at query time

def main(q_id, collection_name, query_text):
    print(q_id + " " + collection_name+ " " + query_text)
    MIN_RESULT_LENGTH = 10
    OUT_DIR = "testbed/"
    RESULT_FILE = "control_results.txt"
    if parameters.use_thesaurus:
        RESULT_FILE = "thesaurus_results.txt"

    # construct collection and query
    query_id = q_id
    collection = collection_name
    query = query_text

    # clean query
    if parameters.case_folding:
       query = query.lower ()
    query = re.sub (r'[^ a-zA-Z0-9]', ' ', query)
    query = re.sub (r'\s+', ' ', query)
    query_words = query.split (' ')

    # Check if using thesaurus
    # Design is to get synonyms for each query term,
    # Excluding synonyms that are longer than one word, as the breaking
    # Up of many words into their constituent words
    # Might not make sense as a synonym.
    # Particularly since the system search on term basis and not a phrase basis

    if parameters.use_thesaurus:
        added_synonyms = []
        for term in query_words:
            thesaurus = py_thesaurus.WordAnalyzer(term)
            synonyms = thesaurus.get_synonym()
            # ignore synonyms that are more than one word long
            allowed_synonyms = []
            for s in synonyms:
                if(len(s.split(" ")) == 1):
                    allowed_synonyms.append(s)
            for s in allowed_synonyms:
                if s not in added_synonyms:
                    added_synonyms.append(s)
        query_words.extend(added_synonyms) # list of synonyms for a word

    # create accumulators and other data structures
    accum = {}
    filenames = []
    p = porter.PorterStemmer ()

    # get N
    f = open (collection+"_index_N", "r")
    N = eval (f.read ())
    f.close ()

    # get document lengths/titles
    titles = {}
    f = open (collection+"_index_len", "r")
    lengths = f.readlines ()
    f.close ()

    # get index for each term and calculate similarities using accumulators
    for term in query_words:
        if term != '':
            if parameters.stemming:
                term = p.stem (term, 0, len(term)-1)
            if not os.path.isfile (collection+"_index/"+term):
               continue
            f = open (collection+"_index/"+term, "r")
            lines = f.readlines ()
            idf = 1
            if parameters.use_idf:
               df = len(lines) # document frequency of a word
               idf = 1/df
               if parameters.log_idf:
                  idf = math.log (1 + N/df)
            for line in lines:
                mo = re.match (r'([0-9]+)\:([0-9\.]+)', line)
                if mo:
                    file_id = mo.group(1)
                    tf = float (mo.group(2))
                    if not file_id in accum:
                        accum[file_id] = 0
                    if parameters.log_tf:
                        tf = (1 + math.log (tf))
                    accum[file_id] += (tf * idf)
            f.close()

    # parse lengths data and divide by |N| and get titles
    for l in lengths:
       mo = re.match (r'([0-9]+)\:([0-9\.]+)\:(.+)', l)
       if mo:
          document_id = mo.group (1)
          length = eval (mo.group (2))
          title = mo.group (3)
          if document_id in accum:
             if parameters.normalization:
                accum[document_id] = accum[document_id] / length
             titles[document_id] = title

    # print top ten results
    result = sorted (accum, key=accum.__getitem__, reverse=True)
    for i in range (min (len (result), MIN_RESULT_LENGTH)):
       print ("{0:10.8f} {1:5} {2}".format (accum[result[i]], result[i], titles[result[i]]))

    def write_to_result_file(result, query_id):
        run_id  = "control"
        output = OUT_DIR + RESULT_FILE
        if parameters.use_thesaurus:
            run_id = "thesaurus"
        if not os.path.isdir(OUT_DIR):
            os.mkdir("testbed")
            output = "testbed/"+RESULT_FILE
            print("Writing results to: " + output)
        else:
            print("Writing results to: " + output)
        with open(output, "a") as f:
            for i in range(min(len(result), MIN_RESULT_LENGTH)):
                # <query-id> <literal '0'> <document-id> <rank> <score> <run-id>
                f.write(str(query_id) + " 0 " + str(result[i]) + " " + str(i) + " " + str(accum[result[i]]) + " " + run_id+"\n")
        f.close()

    write_to_result_file(result, query_id)

if __name__=='__main__':
    # check parameter for collection name
    if len(sys.argv) < 4:
        print("Syntax: query.py <query-id> <collection> <query>")
        exit(0)
    sys.exit(main(sys.argv[1], sys.argv[2], sys.argv[3:]))