"""
 SECTION: Libraries
 These libraries are needed for program execution
 NLTK: Tokenization of the data
 String: String manipulation functions
 CSV: Export to CSV for testing
 Operator: For sorting through dicts
 Re: For regular expressions used to remove tags
 Collections: Used for dict creation and custom data structure creation
 Pandas: Used for dataframes. Better for pretty print and sorting
 Sys: For passing arguments to the program
"""
import nltk
from nltk.tokenize import word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords
import csv
import operator
import re
import pandas
import collections
from collections import defaultdict, Counter
import sys

# Turns the text file into a usable input
def get_input(filepath):
    # Open the filepath in a read fashion
    f = open(filepath, 'r')
    # Read the file
    content = f.read()
    # Return the file as a list
    return content
"""
    This function is main nucleus of the program
    It will calculate the number of paragraphs, collection and document frequencies, and returned a merged dictionary
    This program first tokenizes the input file into paragraphs
    It then tokenizes each paragraph into words
    It utilizes NLTK, collections, and operator
"""
def get_frequencies(myfile):
    #Reg Exp Tested on: https://pythex.org/
    p = r'<P ID=\d+>(.*?)</P>'
    # Create a tokenizer (based on the regular expression for paragraph tags)
    paras = RegexpTokenizer(p)
    # Tokenize the input file into paragraphs, and count the length of the list of tokens to get
    # the # of paragraphs
    num_paragraphs = len(paras.tokenize(myfile))
    # Now create a tokenizer for a word
    # Utilize NLTK's RegexpTokenizer to account for things like punctuation and special characters
    words = RegexpTokenizer(r'\w+')
    # Create collection and document frequency counter objects
    collection_frequency = collections.Counter()
    document_frequency = collections.Counter()
    # Now tokenize the file by paragraph
    for para in paras.tokenize(myfile):
        # Loop through each paragraph and tokenize each word
        # Also, lowercase it
        tokens = [word.lower() for word in words.tokenize(para)]
        # Update the collection frequency by adding a word to it
        collection_frequency.update(tokens)
        # Update the document frequency by adding a set of words to it
        document_frequency.update(set(tokens))

    # Create a merged dictionary
    merged_dictionary = {word:(collection_frequency[word], document_frequency[word]) for word in collection_frequency}

    # Return all of the data
    return num_paragraphs, collection_frequency, document_frequency, merged_dictionary

# This function cleans a dict and removes any stop words
def clean_dict(mydict, mylist):
    #Influenced by: https://stackoverflow.com/questions/1688863/deleting-from-dict-if-found-in-new-list-in-python
    # Loop through the given list (of stop words)
    for word in mylist:
        # If the current word is a key in the dictionary
        if (word in mydict.keys()):
            # Pop the key (and its value) out of the dictionary
            mydict.pop(word)
        # Otherwise
        else:  
            # Keep going
            continue
    
    # Return the cleaned dict
    return mydict

# This function finds the intersetion of two lists
def intersection(l1, l2):
    # Blank list to return containing items in both lists
    in_both = []
    # Recreate the first list with just the first item in a tuple
    # Needed since the given lists are lists of tuples
    list1 = [i[0] for i in l1]
    # Recreate the second list with just the first item in a tuple
    # Needed since the given lists are lists of tuples
    list2 = [i[0] for i in l2]

    # Now loop through the first list
    for item in list1:
        # If that is also in the second list
        # Meaning it is in both files' top 100
        if (item in list2):
            # Append it to the in_both list
            in_both.append(item)
        # Otherwise
        else:
            # Keep going
            continue
    
    # Return the list containing items in both
    return in_both

# This function sorts a dictionary object
def sort_dictionary(mydict):
    # This code was actually inspired by an article below:
    # Inspired by: https://www.w3resource.com/python-exercises/dictionary/python-data-type-dictionary-exercise-1.php
    # Order the dictionary in a list
    # It sorts the items in a (list of) tuple format in reverse (descending) order on the 1 index (frequency) item
    ordered_dict = sorted(mydict.items(), key=operator.itemgetter(1), reverse=True)
    # Turn it back into a dictionary
    dict(ordered_dict)

    # Return it
    return ordered_dict

# This function searches a dictionary for a term
def search_dictionary(mydict, term):
    # Inspired by: https://stackoverflow.com/questions/44664247/python-dictionary-how-to-get-all-keys-with-specific-values
    # Create a list of dictionary keys that match the search term
    words = [k for k, v in mydict.items() if v == term]
    return len(words)

# Driver Program
def driver(file, other_file):
    # Load the data from the text file
    myfile = get_input(file)
    myfile2 = get_input(other_file)
    
    # ## ANSWERS
    # Collect to the number of paragraphs, collection and document frequencies by word, and a merged dictionary
    num_paragraphs, collection_frequency, document_frequency, merged_frequencies = get_frequencies(myfile)
    num_paragraphs2, collection_frequency2, document_frequency2, merged_frequencies2 = get_frequencies(myfile2)
    # Created a sorted dictionary (by collection frequency descending, with document frequency, grouped by word)
    sorted_collection_frequency = sort_dictionary(merged_frequencies)

    # Create a list (set) of English stop words
    stop_words = set(stopwords.words('english'))

    # Create the two "dirty" (with stop words included) top 100 lists from both files
    dict1 = sort_dictionary(collection_frequency)
    dict2 = sort_dictionary(collection_frequency2)
    dict1_top = dict1[:100]
    dict2_top = dict2[:100]

    # Create the the two "clean" (with stop words removed) top 100 lists from both files
    collection_frequency_cleaned = clean_dict(collection_frequency, stop_words)
    collection_frequency_cleaned2 = clean_dict(collection_frequency2, stop_words)    
    dict1_cleaned = sort_dictionary(collection_frequency_cleaned)
    dict1_cleaned_top = dict1_cleaned[:100]
    dict2_cleaned = sort_dictionary(collection_frequency_cleaned2)
    dict2_cleaned_top = dict2_cleaned[:100]

    # Print out requested data
    both = intersection(dict1_top, dict2_top)
    both_cleaned = intersection(dict1_cleaned_top, dict2_cleaned_top)
    print(both)
    print()
    print(both_cleaned)

# Main Program
def main():

    # Use argument as the filename or filepath
    driver(sys.argv[1], sys.argv[2])

# Call main
main()