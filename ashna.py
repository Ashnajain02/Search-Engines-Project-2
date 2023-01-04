#Ashna Jain
#Homework 2
#446 Fall 2022

import gzip
import math
from collections import Counter
import sys

outlink_dict = {}
page_rank1 = {}
page_rank2 = {}
lamb = 0.2#lamb_input
tau = 0.005#tau_input
inlink_counter = Counter()

with gzip.open('small.srt.gz', "rt") as file:
    #creating outlink_dict and setting all values of page_rank1 & page_rank2 values to 0.
    for line in file:
        page, outlink = line.split()
        #create entry for every new page
        if page not in outlink_dict:
            outlink_dict[page] = [outlink]
            page_rank1[page] = 0
            page_rank2[page] = 0
        else:
            #if page exists, add the new outlink
            outlink_dict[page]+= [outlink]
            page_rank1[page] = 0
            page_rank2[page] = 0
        if outlink not in outlink_dict:
            #check if the oulink is in dict, if no, add it
            #we do this in the case where a page has no outlinks.
            outlink_dict[outlink] = []
            page_rank1[outlink] = 0
            page_rank2[outlink] = 0

        inlink_counter.update([outlink])

    #print(outlink_dict)
    #print(page_rank1)
    #print(page_rank2)

    #initalize all the values of page_rank1 to 1/N
    for page in page_rank1:
        page_rank1[page] = 1 / len(page_rank1)
    #print(page_rank1)

    
    converged = False
    #while not converged
    while converged == False:
        zero_outlinks = 0
        #reset value of page_rank2 to lambda/N
        for page in outlink_dict:
            page_rank2[page] = lamb / len(outlink_dict)
        #for a each page
        for page in outlink_dict:
            #get the outlinks of the page
            outlinks = outlink_dict[page]
            #if it has at least 1 outlink
            if len(outlinks) > 0:
                #distribute it's rank to those page(s)
                distributed_rank = page_rank1[page]/len(outlinks)
                for outlink in outlinks:
                    page_rank2[outlink] += (1 - lamb) * distributed_rank 
            #if it has ZERO outlinks
            else:
                #distribute its rank to all the pages
                #for website in page_rank1:
                    #distributed_rank = page_rank1[page]/len(outlink_dict)
                    #page_rank2[website] += (1 - lamb) * distributed_rank
                distributed_rank = page_rank1[page]/len(outlink_dict)
                zero_outlinks += (1 - lamb) * distributed_rank
            
        for page in page_rank2:
            page_rank2[page] += zero_outlinks
        
        #calcuate converge using L2 Norm
        sum = 0
        for page in page_rank2:
            sum += (page_rank1[page] - page_rank2[page])**2
        sum = math.sqrt(sum)
        if sum < tau:
            converged = True

        #update page_rank1 values from page_rank2 values
        for page in page_rank2:
            page_rank1[page] = page_rank2[page]

#function that reverse a dictionary, new value is count, and not the literal key
def reverse_dict_list(d):
    reversed = {}
    for key, values in d.items():
        for v in values:
            reversed.setdefault(v, 0)
            reversed.setdefault(key, 0)
            reversed[v] = reversed.get(v) + 1
    return reversed

#function that sorts a dict with the top k values using the counter method
def topFrequency(data, k):
    dict = Counter(data)
    return dict.most_common(k)   

with open("inlinks.txt", 'w') as file:
    #file.write(data)
    inlink_dict = topFrequency(reverse_dict_list(outlink_dict), 100)
    rank = 0
    for page, inlinkCount in inlink_dict:
        rank = rank + 1
        file.write(page)
        file.write("\t")
        file.write(str(rank))
        file.write("\t")
        file.write(str(inlinkCount))
        file.write("\n")
    
with open("pagerank.txt", 'w') as file:
    sortedPageRank = topFrequency(page_rank1, 100)
    rank = 0
    for page, overallRank in sortedPageRank:
        rank = rank + 1
        file.write(page)
        file.write("\t")
        file.write(str(rank))
        file.write("\t")
        file.write(str(overallRank))
        file.write("\n")