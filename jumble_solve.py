# jumble_solve.py

# enter words as strings on command line separated by spaces
# works best for works of 7 letters or less.  Uses purely
# linear search, so is not optimized for speed at all!

import itertools
import os
import sys
import time
import tqdm

# jumble = 'nopely'
jumble = sys.argv[1:]    # take remaining arguments after file name...

# this is the master list of words, but it is delineated by \n
# need to strip each line
WORDLIST_FILENAME = '/Users/Olson/bdrive/pythonuser/words2.txt'
lines = (line.rstrip('\n') for line in open(WORDLIST_FILENAME))
master = [x for x in lines]
print '\nUsing master list with %i words...\n' % len(master)

for wordno in jumble:

    # start timer
    t_start = time.time()
    
    # make list of characters in current word
    wlist = list(wordno)

    # create submaster list with only words of length matching input
    # put in all caps since list is irregular
    submaster = []
    for i in range(len(master)):
        if len(master[i]) == len(wlist):
            submaster.append(master[i].upper())
    submaster.sort()
    sl = len(submaster)

    # use the itertools function from 2.6 and later to create all permutations
    # returns an interator object, so need to parse into list
    # then makes a lambda function that returns the ith permutation as a string
    allperms = itertools.permutations(wlist)
    res = [x for x in allperms]
    jnx = lambda i: ''.join(res[i]) # returns ith permutation of wordlist

    # create a list of all possible words
    # put in all caps to match master sublist
    wordlist = []
    for i in range(len(res)):
        wordlist.append(jnx(i).upper())
    wordlist.sort()
    wl =len(wordlist)
    letterstring = '-'.join(wlist).upper()
    print ('There are %i combnations possible with the letters %s.' 
                % (wl, letterstring )    )

    # now we have a master list of English words
    # and a list of all permutations of our letter jumble
    print ('Comparing against submaster list with %i words of length %s...' 
                % (sl, len(wlist))      )

    truelist = []
    for mywordno in tqdm.trange(wl):
        result = [i for i in submaster if wordlist[mywordno] in i]
        if len(result)> 0:
            truelist.append(result)
    print '\r',
    
    # The output of the loops is a list of multiple dimensions
    # this line flattens the list into a single dimension of words    
    # and then collapses duplicates using the set iterator
    chain = list(itertools.chain.from_iterable(truelist) )
    outputlist = list(set(chain))
    
    t_stop = time.time()
    elapsed = t_stop - t_start

    print ('%4.1f sec:\t %s ---->\t%s \n' % 
        (elapsed, letterstring, outputlist)   )
