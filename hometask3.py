import re

# declare variable with the text
task_text = '''homEwork:
	tHis iz your homeWork, copy these Text to variable. 

	You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.

	it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE. 

	last iz TO calculate nuMber OF Whitespace characteRS in this Text. caREFULL, not only Spaces, but ALL whitespaces. I got 87.
'''

# Split the text by \n\n and remove leading and trailing spaces
paragraphs = task_text.strip().split('\n\n')
# declare empty list to be appended with normalized text
normalized_paragraphs = []

# for loop goes through splited paragraphs and splits them into sentences
for p in paragraphs:
    sentences = p.strip().split('. ')
    normalized_sentences = []
    for sentence in sentences: # for loop goes through sentences if they are not empty and capitalized first letter of the sentence and maked the rest sentence lower case
        sentence = sentence.strip()
        if sentence:
            normalized = sentence[0].upper() + sentence[1:].lower()
            normalized_sentences.append(normalized)
    joined_paragraph = '. '.join(normalized_sentences) # normalized sentences are joined by the same separator as it was split
    normalized_paragraphs.append(joined_paragraph)

normalized_text = '\n\n\t'.join(normalized_paragraphs) # normalized paragraphs are joined into the text
print(normalized_text)


# add new sentence
last_words = re.findall(r'(\w+)\.', normalized_text) # find all last words with regular expression
new_sentence=' '.join(last_words) + '.'  # join found words into a sentence
paragraphs = normalized_text.splitlines() # split the text by lines to be able to add new sentence to the 3rd paragraph
paragraphs[3] += ' ' + new_sentence.capitalize() # add new sentence to the paragraph
added_text = '\n'.join(paragraphs) # join paragraphs back
print(added_text)

# correct error in 'iz'
regex_var = re.search(r'\siz\s',normalized_text).group() # find incorrectly spelled words
replaced_text = normalized_text.replace(regex_var, ' is ') # correct the error
print(replaced_text)

# count number of whitespaces
test_text = re.findall(r'\s', task_text) # find all whitespaces
counted = len(test_text)
print('Total number of whitespaces: ', counted)
