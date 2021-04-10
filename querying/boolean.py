import numpy as np
import json
import sys
from parse_query import *


#json_file = "../indexing/full_index.json"
json_file = "../indexing/partial_index.json"
with open(json_file) as f:
    documents_containing_word = json.load(f)


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
                docs.append(list1[ptr1])
                ptr1 += 1
                ptr2 += 1
            else:
                actual_dist = list2[ptr2][1] - list1[ptr1][1]
                if actual_dist == req_dist:
                    docs.append(list1[ptr1])
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

    return docs


def boolean_retrieval(query):
    '''
    Obtain the postings lists of the words in the phrase
    Sort them in the order of their lengths
    Perform a merge wherever two documents are the same
    Also, in Boolean Retrieval, ignore the values of the key, that is, the second value in each tuple
    '''
    parsed_query = query_parser(query)
    docs_list = []
    for word in parsed_query:
        if word in documents_containing_word:
            docs_list.append(documents_containing_word[word])
        else:
            docs_list.append([])    
    len_list = [len(docs_with_word) for docs_with_word in docs_list]

    # Handle the case when no match
    if len(docs_list) == 0:
        return []

    # For efficiency, sort lists by their sizes, then merge
    sort_by_len = np.argsort(len_list)
    new_docs_list = [None] * len(docs_list)
    for i in range(len(docs_list)):
        new_docs_list[i] = docs_list[sort_by_len[i]]

    final_list = new_docs_list[0]
    if len(new_docs_list) != 1:
        for i in range(1, len(new_docs_list)):
            final_list = merge(final_list, new_docs_list[i])
    
    final_docs = []
    for i in range(len(final_list)):
        if i != 0:
            if final_list[i][0] != final_docs[-1]:
                final_docs.append(final_list[i][0])
        else:
            final_docs.append(final_list[0][0]) 

    return final_docs

def phrase_retr(phrase):
    '''
    Obtain the postings lists of the words in the phrase
    Sort them in the order of their lengths
    Perform a merge wherever two documents are the same, and their positions in the given document have the required distance
    '''
    parsed_phrase = query_parser(phrase)    

    # Repeat words in a phrase not handled
    ctr = 0
    word_pos = dict()
    for word in parsed_phrase:
        word_pos[word] = ctr
        ctr += 1
    
    docs_list = []
    for word in parsed_phrase:
        if word in documents_containing_word:
            docs_list.append(documents_containing_word[word])
        else:
            docs_list.append([])    
    len_list = [len(docs_with_word) for docs_with_word in docs_list]

    # Handle the case when no match
    if len(docs_list) == 0:
        return []

    # For efficiency, sort lists by their sizes, then merge
    sort_by_len = np.argsort(len_list)
    new_docs_list = [None] * len(docs_list)
    for i in range(len(docs_list)):
        new_docs_list[i] = docs_list[sort_by_len[i]]

    final_list = new_docs_list[0]
    if len(new_docs_list) != 1:
        for i in range(1, len(new_docs_list)):
            distance = sort_by_len[i] - sort_by_len[0]
            final_list = merge(final_list, new_docs_list[i], distance)

    final_docs = []
    for i in range(len(final_list)):
        if i != 0:
            if final_list[i][0] != final_docs[-1]:
                final_docs.append(final_list[i][0])
        else:
            final_docs.append(final_list[0][0]) 
            
    return final_docs

# Comment out this line if needed
print("Write queries")
while(True):
    query = input()
    print(len(boolean_retrieval(query)))