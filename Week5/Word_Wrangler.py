'''
student code for Word Wrangler game
'''

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = 'assets_scrabble_words3.txt'


# functions to manipulate ordered word lists

def remove_duplicates(list1):
    '''
    eliminate (function can be iterative) duplicates in a sorted list;
    returns a new sorted list with the same elements in list1, without duplicates
    '''
    screened = []
    for item in list1:
        # screening for duplicating items
        if item not in screened:
            screened.append(item)

    return screened

def intersect(list1, list2):
    '''
    compute (this function can be iterative) the intersection of two sorted lists;
    returns a new sorted list containing only elements that are in  both list1 and list2
    '''
    screened = []
    for item in list1:
        # checking for items in common
        if item in list2:
            screened.append(item)
            
    return screened


# functions to perform merge sort

def merge(list1, list2):
    '''
    merge (function can be iterative) two sorted lists;
    returns a new sorted list containing all of the elements that are in either list1 and list2
    '''
    merged = []
    # making copies to avoid list mutation
    copy1, copy2 = list1[:], list2[:]
    while min(copy1, copy2):
        # adding smaller item (and removing it from its list) one by one
        if copy1[0] < copy2[0]:
            merged.append(copy1[0])
            copy1.pop(0)
        else:
            merged.append(copy2[0])
            copy2.pop(0)

    # must include to whatever has been left in longer list (shorter list is empty by now)
    if copy1:
        merged += copy1
    else:
        merged += copy2
   
    return merged
                
def merge_sort(list1):
    '''
    sort (function shall be recursive!) the elements of list1, makes use of merge() function;
    returns a new sorted list with the same elements as list1
    '''
    # base case; for empty/one item lists
    if len(list1) <= 1:
        return list1
    # finding midsection of the list
    half = len(list1) / 2
    
    return merge(merge_sort(list1[:half]), merge_sort(list1[half:]))
    

# function to generate all strings for the word wrangler game

def gen_all_strings(word):
    '''
    generate (function shall be recursive!) all strings that can be composed
    from the letters in word in any order;
    returns a list of all strings that can be formed from the letters in word
    '''
    # base case; no string
    if not word:
        return ['']
    
    possibilities = []
    # generate all appropriate strings for rest of the word
    for string in gen_all_strings(word[1:]):
        for index in range(len(string) + 1):
            # inserting the initial character in all possible positions within the string
            possibilities.append(string[:index] + word[0] + string[index:])
            
    return gen_all_strings(word[1:]) + possibilities


# function to load words from a file

def load_words(filename):
    '''
    load word list from the file named filename;
    returns a list of strings
    '''
    try:
        opened_file = open(filename)
    except IOError:
        print 'Your scrabble words file is missing.'
     
    return [word[:-1] for word in opened_file]
    
def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# uncomment when you are ready to try the game
# run()
