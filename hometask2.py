import random
import string

# declare an empty list to append with generated dictionaries
dict_list = []

# while loop generates dictionaries and adds them to empty list until the length of the list is less or equals the random value
while len(dict_list) <= random.randint(2, 10):
    list_dict = {} #empty dict is declared to be populated with generated key:value pairs
    while len(list_dict) <= random.randint(1, 26): #while loop generated key:value pairs until dictionary length meets reqs
        randomLetter = random.choice(string.ascii_letters)
        list_dict[randomLetter.lower()] = random.randint(0, 100)
    dict_list.append(list_dict)

# declare empty dictionary which will be populated with key-value pairs from the list
new_dict = {}
key_lst = []

# for loop generates a list with all the keys from dict_list
for dct in dict_list:
    for key in dct.keys():
        key_lst.append(key)


for dct in dict_list:
    dict_keys = set(dct.keys())
    # iterate over the keys of each dict in the list
    for key in dict_keys:
        if key_lst.count(key) > 1:
            # if there are more than 1 key occurrences in all the dicts, generate the new key
            new_key = key + '_' + str(dict_list.index(dct)+1)
            # replace the pair with the new key and the same val
            dct[new_key] = dct.pop(key)
    new_dict.update(dct)

for key in set(key_lst):
    # if there are > 1 key initially
    if key_lst.count(key) > 1:
        # get max(val) for these keys
        max_val = max([val for k, val in new_dict.items() if key in k])  # find max(val) for all the same keys
        # delete pairs with val != max(val)
        new_dict = {k : v for k, v in new_dict.items() if key not in k or v == max_val}


print(new_dict)