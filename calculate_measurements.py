'''
Calculate Precison, Recall, MAP and NDCG for all 3 queries.
Reads from testbed results files.
'''

#imports
import os

TARGET_DIR = "testbed/"

class run:

    query_id = -1
    doc_id = -1
    rank = -1
    score = -1
    run_id = "none"

    def __init__(self, query_id, doc_id, rank, score, run_id):
        self.query_id = query_id
        self.doc_id = doc_id
        self.rank = rank
        self.score = score
        self.run_id = run_id

    def __str__(self):
        return str(self.query_id)+ " " + str(self.doc_id) + " " + str(self.rank)+ " " + str(self.score)+ " " + str(self.run_id)


class relevance:
    # Trec relevance format:
    # <query-id> <literal '0'> <document-id> <document relevance>
    query_id = -1
    doc_id = -1
    rel_value = -1

    def __init__(self, query_id, doc_id, rel_value):
        self.query_id = query_id
        self.doc_id = doc_id
        self.rel_value = rel_value

    def __str__(self):
        return str(self.query_id) + " " + str(self.doc_id) + " " + str(self.rel_value)

    def get_relevance(self, run_obj):
        if run_obj.query_id == self.query_id and run_obj.doc_id == self.doc_id:
            return self.rel_value
        return -1


relevance_judgements = []
control_run = []
thes_run = []
'''
Read in list or string of filenames
based on if it is a run file or judgment file
'''
def readfiles(filenames, runfiles):
    if type(filenames) == list:
        count = 1
        for file in filenames:
            if os.path.isfile(file):
                with open(file, "r") as f:
                    lines = f.readlines()
                    # for both skip literal '0' at pos 1
                    if(runfiles):
                        # <query-id> <literal '0'> <document-id> <rank> <score> <run-id>
                        for l in lines:
                            parts = l.split(" ")
                            run_obj = run(parts[0], parts[2], parts[3], parts[4], parts[5])
                            if(count == 1):
                                control_run.append(run_obj)
                            elif(count == 2):
                                thes_run.append(run_obj)
                        count = count + 1

                    else:
                        # <query-id> <literal '0'> <document-id> <document relevance>
                        for l in lines:
                            parts = l.split(" ")
                            rel_obj = relevance(parts[0], parts[2], parts[3])
                            relevance_judgements.append(rel_obj)
                f.close()
            else:
                print("Could not open file: "+file)

    else:
        print("Expected list of one or more filenames")
        return

readfiles([TARGET_DIR+"control_results.txt", TARGET_DIR+"thesaurus_results.txt"], True)
readfiles([TARGET_DIR+"trec_relevance_judgements.txt"], False)

def get_number_relevant_and_retrieved(run_objs, rel_objs, q_id):
    count = 0
    for i in run_objs:
        for j in rel_objs:
            if i.query_id == q_id and j.query_id == q_id:
                if j.get_relevance(i) >= 1:
                    count = count + 1
    return count

'''
Calculates Precison for all the queries.
Precision is the fraction of retrieved documents that are relevant to the query.
Take in flag to indicate if control or not
Threshold for relevant document is geq to 1.
'''
def calculate_precision(iscontrol):
    precision_per_q_dic = {}
    if(iscontrol):
        for obj in control_run:
            qid = obj.query_idS
            if qid not in precision_per_q_dic.keys():
                num_retrieved = 0
                for i in control_run:
                    if i.query_id == obj.query_id:
                        num_retrieved += num_retrieved + 1
                denom = get_number_relevant_and_retrieved(control_run, relevance_judgements, qid)
                if denom > 0:
                    precision_per_q_dic[qid] = num_retrieved / denom
                else:
                    precision_per_q_dic[qid] = 0
    else:
        for obj in thes_run:
            qid = obj.query_idS
            if qid not in precision_per_q_dic.keys():
                num_retrieved = 0
                for i in thes_run:
                    if i.query_id == obj.query_id:
                        num_retrieved += num_retrieved + 1
                denom = get_number_relevant_and_retrieved(thes_run, relevance_judgements, qid)
                if denom > 0:
                    precision_per_q_dic[qid] = num_retrieved / denom
                else:
                    precision_per_q_dic[qid] = 0
    return precision_per_q_dic



