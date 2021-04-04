import sys
import csv
import pandas as pd
import re

file_count = 10
redundant_entries = dict()

def write_prof_data_to_csv(output_file, professor_data_to_write):
    try:
        write = csv.writer(output_file)
        write.writerow(professor_data_to_write)
    except:        
        pass

def check_for_nan(input_string):
    if pd.isna(input_string):
        return ''
    else:
        return input_string

def make_list(initial_string):   

    svg_tag = re.compile(", <svg.*svg>, '")     
    html_tags = re.compile(", <.*>, '") 
    html_tags_inside = re.compile("<.*>.*</.*>")
    splitter = re.compile("[\"'], [\"']")  

    svg_removed =  svg_tag.sub(', \'\', \'',initial_string)
    html_removed = html_tags.sub(', \'', svg_removed)   
    plain_text = html_tags_inside.sub('', html_removed)

    return splitter.split(plain_text.lstrip('[\'').rstrip('\']'))     

def make_list_citations(initial_string):
    try:
        return list(map(int,initial_string.lstrip('[').rstrip(']').split(', ')))
    except:
        return []

for file_index in range(file_count):    

    try:
        input_file = pd.read_csv('../scraping/professor_data-'+str(file_index)+'.csv',header=None,encoding='utf8')
        output_file = open('professor_data-'+str(file_index)+'-cleaned.csv', 'w+',newline ='',encoding='utf8')
    except:
        print("Error in opening input/output file.")
        sys.exit(0)

    number_of_professors = len(input_file)    

    scholar_ids = set()     
    
    for prof_index in range(number_of_professors):            

        scholar_id = input_file.iloc[prof_index][0]
        name = check_for_nan(input_file.iloc[prof_index][1])
        image_url = check_for_nan(input_file.iloc[prof_index][2])
        affiliation = check_for_nan(input_file.iloc[prof_index][3])
        email = check_for_nan(input_file.iloc[prof_index][4])
        homepage = check_for_nan(input_file.iloc[prof_index][5])
        topics_list = make_list(input_file.iloc[prof_index][6])
        cit = int(input_file.iloc[prof_index][7])
        h_ind = int(input_file.iloc[prof_index][8])
        i_ind = int(input_file.iloc[prof_index][9])
        cit5 = int(input_file.iloc[prof_index][10])
        h_ind5 = int(input_file.iloc[prof_index][11])
        i_ind5 = int(input_file.iloc[prof_index][12])    
        cit_list = make_list_citations(input_file.iloc[prof_index][13])
        image_url = check_for_nan(input_file.iloc[prof_index][14])
        papers_url_list = make_list(input_file.iloc[prof_index][15])
        papers_title_list = make_list(input_file.iloc[prof_index][16])              

        if scholar_id in scholar_ids:            
            if file_index not in redundant_entries:
                redundant_entries[file_index]=1
            else:
                redundant_entries[file_index]+=1            
        else:
            if len(papers_url_list)!=len(papers_title_list):
                continue                            
            scholar_ids.add(scholar_id)
            professor_data_to_write = (scholar_id, name, image_url, affiliation, email, homepage, topics_list, cit, h_ind, i_ind, cit5, h_ind5, i_ind5, cit_list, image_url, papers_url_list, papers_title_list)    
            write_prof_data_to_csv(output_file, professor_data_to_write)

for file_index in redundant_entries:
    print("Removed "+str(redundant_entries[file_index])+" reduntant entries from file "+str(file_index))