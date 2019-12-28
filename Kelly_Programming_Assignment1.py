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
    print(type(content))
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

# This function calculates the size of the vocabulary
def vocabulary_size(mydict):
    # Return the length of the dictionary passed in
    return len(mydict)

# This function is a helper function that prints a dict structure to a file
# This was used mainly for confirmation of correct program execution
def dict_to_file(mydict, name):
    w = csv.writer(open("D:\\Grad School\\Fall 2019\\605.744.81.FA19 - Information Retrieval\Module 1\\{}.csv".format(name), "w", newline = ''))
    for key, val in mydict.items():
        w.writerow([key, val])

# This function is a helper function that prints a list structure to a file
# Thised was used mainly for confirmation of correct program execution
def list_to_file(mylist, name):
    with open("D:\\Grad School\\Fall 2019\\605.744.81.FA19 - Information Retrieval\Module 1\\{}.csv".format(name), 'w') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(mylist)

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
def driver(file):
    # Load the data from the text file
    myfile = get_input(file)

    # ## ANSWERS
    # Collect to the number of paragraphs, collection and document frequencies by word, and a merged dictionary
    num_paragraphs, collection_frequency, document_frequency, merged_frequencies = get_frequencies(myfile)
    # Created a sorted dictionary (by collection frequency descending, with document frequency, grouped by word)
    sorted_collection_frequency = sort_dictionary(merged_frequencies)

    # Print out requested data
    print("\nNumber of Paragraphs Processed: {}".format(num_paragraphs))
    print("\nNumber of Unique Words (Vocabulary Size): {}".format(vocabulary_size(merged_frequencies)))
    print("\nNumber of Total Words (Collection Size): {}".format(sum(collection_frequency.values())))
    # NOTE - Did not print out the collection and document frequency by word due to
    # assignment instructions not specifying REPORT them, but to simply calculate them
    #print("\nCollection Frequency (by word): {}".format(collection_frequency))
    #print("\nDocument Frequency (by word): {}".format(document_frequency))
    print("\nMost Frequent Words: {}".format(sorted_collection_frequency[:100]))
    print("\n500th Word: {}".format(sorted_collection_frequency[499]))
    print("\n1000th Word: {}".format(sorted_collection_frequency[999]))
    print("\n5000th Word: {}".format(sorted_collection_frequency[4999]))
    print("\nNumber of Items that only appear in one paragraph: {}".format(search_dictionary(document_frequency, 1)))

# Main Program
def main():

    # Use argument as the filename or filepath
    driver(sys.argv[1])

# Call main
main()