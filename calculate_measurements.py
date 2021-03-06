'''
Calculate Precison, Recall, MAP and NDCG for all 3 queries.
Reads from testbed results files.
'''

#imports
import os
import math
import pandas

TARGET_DIR = "testbed/"

class run:

    query_id = -1
    doc_id = -1
    rank = -1
    score = -1
    run_id = "none"

    def __init__(self, query_id, doc_id, rank, score, run_id):
        self.query_id = int(query_id)
        self.doc_id = int(doc_id)
        self.rank = int(rank)
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
        self.query_id = int(query_id)
        self.doc_id = int(doc_id)
        self.rel_value = int(rel_value)

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

def get_all_queries(run_obj):
    seen = []
    for obj in run_obj:
        qid = obj.query_id
        if qid not in seen:
            seen.append(qid)
    return seen

def get_number_retrieved_all(run_obj):
    return len(run_obj)

def get_number_relevant_and_retrieved_for_qid(run_objs, rel_objs, q_id):
    count = 0
    for i in run_objs:
        for j in rel_objs:
            if i.query_id == q_id and j.query_id == q_id and j.doc_id == i.doc_id:
                if j.get_relevance(i) >= 1:
                    count = count + 1
    return count

def get_number_relevant_for_qid(rel_objs, q_id):
    count = 0
    for i in rel_objs:
        if i.query_id == q_id:
            if i.get_relevance(i) >= 1:
                count = count + 1
    return count

def get_number_relevant_and_retrieved_for_all(run_objs, rel_objs, all_queries):
    count = 0
    for i in run_objs:
        for j in rel_objs:
            for q in all_queries:
                if i.query_id == q and j.query_id == q:
                    if j.get_relevance(i) >= 1:
                        count = count + 1
    return count

def get_number_relevant_for_all(rel_objs):
    count = 0
    for i in rel_objs:
        if i.get_relevance(i) >= 1:
            count = count + 1
    return count

def get_num_retrieved_for_qid(run_objs, qid):
    num_retrieved = 0
    for obj in run_objs:
        if obj.query_id == qid:
            num_retrieved += 1
    return num_retrieved
'''
Calculates Precision for all the queries.
Precision is the fraction of retrieved documents that are relevant to the query.
Take in flag to indicate if control or not
Threshold for relevant document is geq to 1.
'''
def calculate_precision(iscontrol):
    precision_per_q_dic = {}
    if(iscontrol):
        for obj in control_run:
            qid = obj.query_id
            if qid not in precision_per_q_dic.keys():
                num_retrieved = get_num_retrieved_for_qid(control_run, qid)
                numerator = get_number_relevant_and_retrieved_for_qid(control_run, relevance_judgements, qid)
                precision_per_q_dic[qid] = numerator / num_retrieved
    else:
        for obj in thes_run:
            qid = obj.query_id
            if qid not in precision_per_q_dic.keys():
                num_retrieved = get_num_retrieved_for_qid(thes_run, qid)
                numerator = get_number_relevant_and_retrieved_for_qid(thes_run, relevance_judgements, qid)
                precision_per_q_dic[qid] = numerator / num_retrieved
    return precision_per_q_dic

def calculate_recall(iscontrol):
    recall_per_q_dic = {}
    if (iscontrol):
        for obj in control_run:
            qid = obj.query_id
            if qid not in recall_per_q_dic.keys():
                numerator = get_number_relevant_and_retrieved_for_qid(control_run, relevance_judgements, qid)
                denominator = get_number_relevant_for_qid(relevance_judgements, qid)
                recall_per_q_dic[qid] = numerator / denominator
    else:
        for obj in thes_run:
            qid = obj.query_id
            if qid not in recall_per_q_dic.keys():
                numerator = get_number_relevant_and_retrieved_for_qid(thes_run, relevance_judgements, qid)
                denominator = get_number_relevant_for_qid(relevance_judgements, qid)
                recall_per_q_dic[qid] = numerator / denominator
    return recall_per_q_dic

def calculate_precision_all(iscontrol):
    precision = 0
    if (iscontrol):
        num_retrieved = get_number_retrieved_all(control_run)
        numerator = get_number_relevant_and_retrieved_for_all(control_run, relevance_judgements, get_all_queries(control_run))
        precision = numerator/num_retrieved
    else:
        num_retrieved = get_number_retrieved_all(thes_run)
        numerator = get_number_relevant_and_retrieved_for_all(thes_run, relevance_judgements, get_all_queries(thes_run))
        precision = numerator / num_retrieved

    return precision

def calculate_recall_all(iscontrol):
    recall = 0
    if (iscontrol):
        numerator = get_number_relevant_and_retrieved_for_all(control_run, relevance_judgements, get_all_queries(control_run))
        recall = numerator/get_number_relevant_for_all(relevance_judgements)
    else:
        numerator = get_number_relevant_and_retrieved_for_all(thes_run, relevance_judgements, get_all_queries(thes_run))
        recall = numerator / get_number_relevant_for_all(relevance_judgements)
    return recall

def get_AP (iscontrol, qid):
    ap_list = []
    if (iscontrol):
        count = 1
        rel_and_ret_count = 0
        for i in control_run:
            if(i.query_id == qid):
                for j in relevance_judgements:
                    if(j.query_id == qid and j.doc_id == i.doc_id):
                        if j.get_relevance(i) >= 1:
                            rel_and_ret_count += 1
                        ap_list.append(rel_and_ret_count / count)
                count += 1
    else:
        count = 1
        rel_and_ret_count = 0
        for i in thes_run:
            if (i.query_id == qid):
                for j in relevance_judgements:
                    if(j.query_id == qid and j.doc_id == i.doc_id):
                        if j.get_relevance(i) >= 1:
                            rel_and_ret_count += 1
                        ap_list.append(rel_and_ret_count / count)
                count += 1
    return sum(ap_list)/len(ap_list)

def calculate_MAP(iscontrol):
    map = 0
    queries = get_all_queries(control_run)
    if (iscontrol):
        numerator = 0
        for q in queries:
            numerator += get_AP(True, q)
        map = numerator/len(queries)
    else:
        queries = get_all_queries(thes_run)
        numerator = 0
        for q in queries:
            numerator += get_AP(False, q)
        map = numerator / len(queries)

    return map

def get_ideal_judgements_perq(queries):
    ideal_judgements = {}
    for q in queries:
        judgements = []
        for r in relevance_judgements:
            if r.query_id == q:
                judgements.append(r.rel_value)
        ideal_judgements[q] = sorted(judgements, key=lambda x: x, reverse=True)
    return ideal_judgements

def calculate_NDCG(iscontrol, queries):
    NDCG = {}
    DCG_dic = {}
    IDCG_dic = {}
    given_judgements = {}
    ideal_judgements = get_ideal_judgements_perq(queries)
    if(iscontrol):
        for i in control_run:
            qid = i.query_id
            if qid not in given_judgements.keys():
                judgements = []
                for j in control_run:
                    for r in relevance_judgements:
                        if r.query_id == qid and qid == j.query_id and r.doc_id == j.doc_id:
                            judgements.append(r.rel_value)

                given_judgements[qid] = judgements

        dcg = 0
        idcg = 0
        i = 1
        for q in queries:
            for rel in given_judgements[q]:
                dcg += rel / math.log2(i + 1)
                i += 1
            DCG_dic[q] = dcg
            dcg = 0
            i = 1

        i = 1
        for q in queries:
            for rel in ideal_judgements[q]:
                idcg += rel / math.log2(i + 1)
                i += 1
            IDCG_dic[q] = idcg
            idcg = 0
            i = 1
        for q in queries:
            NDCG[q] = DCG_dic[q]/IDCG_dic[q]
        return NDCG

    else:
        for i in thes_run:
            qid = i.query_id
            if qid not in given_judgements.keys():
                judgements = []
                for j in thes_run:
                    for r in relevance_judgements:
                        if r.query_id == qid and qid == j.query_id and r.doc_id == j.doc_id:
                            judgements.append(r.rel_value)
                given_judgements[qid] = judgements
        dcg = 0
        idcg = 0
        i = 1
        for q in queries:
            for rel in given_judgements[q]:
                dcg += rel / math.log2(i + 1)
                i += 1
            DCG_dic[q] = dcg
            dcg = 0
            i = 1

        i = 1
        for q in queries:
            for rel in ideal_judgements[q]:
                idcg += rel / math.log2(i + 1)
                i += 1
            IDCG_dic[q] = idcg
            idcg = 0
            i = 1
        for q in queries:
            NDCG[q] = DCG_dic[q]/IDCG_dic[q]
        return NDCG

# Save calculated into dics per algorithm
all_queries = get_all_queries(control_run)
control_precision = calculate_precision(True)
thes_precision = calculate_precision(False)
control_recall = calculate_recall(True)
thes_recall = calculate_recall(False)
control_MAP = calculate_MAP(True)
thes_MAP = calculate_MAP(False)
control_NDCG = calculate_NDCG(True, all_queries)
thes_NDCG = calculate_NDCG(False, get_all_queries(thes_run))
control_NDCG_All = sum(control_NDCG.values())/len(control_NDCG)
thes_NDCG_All = sum(thes_NDCG.values())/len(thes_NDCG)

# Print results nicely
print("Number Retrieved")
print("{}\t{}".format("Query", "Control")+"\t\t{}".format("Thesaurus"))
for q in all_queries:
    print("{}\t\t{}".format(q, get_num_retrieved_for_qid(control_run,q))+"\t\t\t{}".format(get_num_retrieved_for_qid(thes_run, q)))
print()

print("Number Relevant")
print("{}\t{}".format("Query", "Number"))
for q in all_queries:
    print("{}\t\t{}".format(q, get_number_relevant_for_qid(relevance_judgements, q)))
print()

print("Number Relevant and Retrieved")
print("{}\t{}".format("Query", "Control")+"\t\t{}".format("Thesaurus"))
for q in all_queries:
    print("{}\t\t{}".format(q, get_number_relevant_and_retrieved_for_qid(control_run,relevance_judgements, q))+"\t\t\t{}".format(get_number_relevant_and_retrieved_for_qid(thes_run,relevance_judgements, q)))
print()

print("Precision")
print("{}\t{}".format("Query", "Control")+"\t\t{}".format("Thesaurus"))
for q in control_precision:
    print("{}\t\t{:f}".format(q, control_precision[q])+"\t{:f}".format(thes_precision[q]))
print()

print("Recall")
print("{}\t{}".format("Query", "Control")+"\t\t{}".format("Thesaurus"))
for q in control_recall:
    print("{}\t\t{:f}".format(q, control_recall[q])+"\t{:f}".format(thes_recall[q]))
print()

print("MAP")
print("{}\t{}".format("Query", "Control")+"\t\t{}".format("Thesaurus"))
for q in all_queries:
    print("{}\t\t{:f}".format(q, get_AP(True, q))+"\t{:f}".format(get_AP(False, q)))
print()

print("MAP All")
print("{}\t{}".format("Query", "Control")+"\t\t{}".format("Thesaurus"))
print("All\t\t{:f}".format( control_MAP)+"\t{:f}".format(thes_MAP))
print()

print("NDCG")
print("{}\t{}".format("Query", "Control")+"\t\t{}".format("Thesaurus"))
for q in control_NDCG:
    print("{}\t\t{:f}".format(q, control_NDCG[q])+"\t{:f}".format(thes_NDCG[q]))
print()

print("NDCG All")
print("{}\t{}".format("Query", "Control")+"\t\t{}".format("Thesaurus"))
print("All\t\t{:f}".format(control_NDCG_All)+"\t{:f}".format(thes_NDCG_All))
print()