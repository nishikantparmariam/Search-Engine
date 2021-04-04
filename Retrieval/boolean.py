import numpy as np
import json
import sys
query_path = "../querying/"
# Insert query_path at position 1
sys.path.insert(1, query_path)

import parse_query.py

def merge(list1, list2, req_dist = None):
    '''
    Given the postings lists of two stemmed words, merge them in the following way.
    AND: Only the documents where both the words appear
    Only the AND merge defined.
    '''
    ptr1 = 0
    ptr2 = 0
    docs = []

    while ptr1 < len(list1) and ptr2 < len(list2):
        if(list1[ptr1][0] == list2[ptr2][0]):
            if req_dist == None:
                docs.append(list1[ptr1][0])
                ptr1 += 1
                ptr2 += 1
            else:
                actual_dist = list2[ptr2][1] - list1[ptr1][1]
                if actual_dist == req_dist:
                    docs.append(list1[ptr1][0])
                    ptr1 += 1
                    ptr2 += 1
                elif actual_dist > req_dist: # This means we need to decrease the actual_dist, or increment the first pointer
                    ptr1 += 1
                elif actual_dist < req_dist: # This means we need to increase the actual_dist, or increment the second pointer
                    ptr2 += 1
        elif list1[ptr1][0] < list2[ptr2][0]:
            ptr1 += 1
        elif list1[ptr1][0] > list2[ptr2][0]:
            ptr2 += 1

    return sorted(list(set(docs)))

def boolean_retrieval(query):
    '''
    Obtain the postings lists of the words in the phrase
    Sort them in the order of their lengths
    Perform a merge wherever two documents are the same
    Also, in Boolean Retrieval, ignore the values of the key, that is, the second value in each tuple
    '''
    parsed_query = parse_query(query)

    docs_list = [documents_containing_word[word] for word in parsed_query]
    len_list = [len(docs_with_word) for docs_with_word in docs_list]

    # For efficiency, sort lists by their sizes, then merge
    sort_by_len = np.argsort(len_list)
    new_docs_list = [None] * len(docs_list)
    for i in range(len(docs_list)):
        new_docs_list[i] = docs_list[sort_by_len[i]]

    final_list = new_docs_list[0]
    if len(new_docs_list) != 1:
        for i in range(1, len(new_docs_list)):
            final_list = merge(final_list, new_docs_list[i])
    return final_list


def phrase_retr(phrase):
    '''
    Obtain the postings lists of the words in the phrase
    Sort them in the order of their lengths
    Perform a merge wherever two documents are the same, and their positions in the given document have the required distance
    '''
    parsed_phrase = parse_query(phrase)

    # Repeat words in a phrase not handled
    ctr = 0
    for word in parsed_phrase:
        word_pos[word] = ctr
        ctr += 1

    docs_list = [documents_containing_word[word] for word in parsed_phrase]
    len_list = [len(docs_with_word) for docs_with_word in docs_list]

    # For efficiency, sort lists by their sizes, then merge
    sort_by_len = np.argsort(len_list)
    new_docs_list = [None] * len(docs_list)
    new_word_pos = [None] * len(word_pos)
    for i in range(len(docs_list)):
        new_docs_list[i] = docs_list[sort_by_len[i]]
        new_word_pos[i] = word_pos[sort_by_len[i]]

    final_list = new_docs_list[0]
    if len(new_docs_list) != 1:
        for i in range(1, len(new_docs_list)):
            distance = new_word_pos[i] - new_word_pos[0]
            final_list = merge(final_list, new_docs_list[i], distance)
    return final_list


# Comment out this line if needed
query = input()

# Open the full file
#json_file = "../indexing/full_index.json"
json_file = "../indexing/partial_index.json"
with open(json_file) as f:
    documents_containing_word = json.load(f)
# Should call this as few times(once) as possible, think about some optimisation
# Something like ifndef in C, the json file should be loaded only once

# The list of all documents corresponding to any word can be found by this
words = [word for word in documents_containing_word.keys()]
