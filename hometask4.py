# refactored home task 2

import random
import string

# declare an empty list to append with generated dictionaries


# the function generates dictionaries of the given length
def create_dict(min_len, max_len):
    list_dict = {}
    while len(list_dict) <= random.randint(min_len, max_len):
        randomLetter = random.choice(string.ascii_letters)
        list_dict[randomLetter.lower()] = random.randint(0, 100)
    return list_dict

# the function generates a list of dict of the given length
def create_list(min_len, max_len):
    dict_list = []
    while len(dict_list) <= random.randint(min_len, max_len):
        dict_list.append(create_dict(1,26))
    return dict_list

# collect all the keys into a list
def collect_all_keys(dict_list):
    key_lst = []
    for dct in dict_list:
        for key in dct.keys():
            key_lst.append(key)
    return key_lst

# check all the keys and if there are more than 1 key rename it
def rename_key(dict_list, key_lst):
    new_dict_list = []
    for i, dct in enumerate(dict_list, start=1):
        new_dct = {}
        for key, value in dct.items():
            if key_lst.count(key) > 1:
                new_key = f"{key}_{i}"
                new_dct[new_key] = value
            else:
                new_dct[key] = value
        new_dict_list.append(new_dct)
    return new_dict_list

# merge all dictionaries from the list into one dict
def merged_dct(dict_list):
    result = {}
    for dct in dict_list:
        result.update(dct)
    return result

# remove all duplicated keys with values < max
def fin_list(dct, key_lst):
    fin_dct = dct.copy()
    for key in set(key_lst):
        if key_lst.count(key) > 1:
            max_val = max(val for k, val in fin_dct.items() if k.startswith(key))
            fin_dct = {k: v for k, v in fin_dct.items()
                          if not k.startswith(key) or v == max_val}
    return fin_dct



init_list_of_dct = create_list(2, 10)

keys_collection = collect_all_keys(init_list_of_dct)

renamed = rename_key(init_list_of_dct,keys_collection)

merged_dict = merged_dct(renamed)

final_dictionary = fin_list(merged_dict, keys_collection)

print(final_dictionary)


# refactored home task 3

import re

# declare variable with the text
task_text = '''homEwork:
	tHis iz your homeWork, copy these Text to variable. 

	You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.

	it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE. 

	last iz TO calculate nuMber OF Whitespace characteRS in this Text. caREFULL, not only Spaces, but ALL whitespaces. I got 87.
'''

# split text by paragraphs, then by sentences, normalize sentences and join back into text
def normalize_paragraph():
    paragraphs = task_text.strip().split('\n\n')
    normalized_paragraphs = []
    for p in paragraphs:
        sentences = p.strip().split('. ')
        normalized_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence:
                normalized = sentence[0].upper() + sentence[1:].lower()
                normalized_sentences.append(normalized)
        joined_paragraph = '. '.join(normalized_sentences)
        normalized_paragraphs.append(joined_paragraph)
    return normalized_paragraphs

normalized_text = '\n\n\t'.join(normalize_paragraph()) # normalized paragraphs are joined into the text
print(f'Task 1: \n {normalized_text}')
#
#
# add new sentence
last_words = re.findall(r'(\w+)\.', normalized_text) # find all last words with regular expression
new_sentence=' '.join(last_words) + '.'  # join found words into a sentence
paragraphs = normalized_text.splitlines() # split the text by lines to be able to add new sentence to the 3rd paragraph
paragraphs[3] += ' ' + new_sentence.capitalize() # add new sentence to the paragraph
added_text = '\n'.join(paragraphs) # join paragraphs back
print(f'Task 2: \n {added_text}')

# correct error in 'iz'
regex_var = re.search(r'\siz\s',normalized_text).group() # find incorrectly spelled words
replaced_text = normalized_text.replace(regex_var, ' is ') # correct the error
print(f'Task 3: \n {replaced_text}')

# count number of whitespaces
test_text = re.findall(r'\s', task_text) # find all whitespaces
counted = len(test_text)
print('Total number of whitespaces: ', counted)
