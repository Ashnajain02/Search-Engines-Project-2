#Ashna Jain
#Homework 2
#446 Fall 2022

import gzip
import math
from collections import Counter
import sys

def main(inputFile, lamb_input, tau_input, inlinksFile, pagerankFile, k):
    outlink_dict = {}
    page_rank1 = {}
    page_rank2 = {}
    lamb = lamb_input
    tau = tau_input

    with gzip.open(inputFile, "rt") as file:
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

        #initalize all the values of page_rank1 to 1/N
        for page in page_rank1:
            page_rank1[page] = 1 / len(outlink_dict)

        converged = False

        while converged == False:
            zero_outlinks = 0

            #reset value of page_rank2 to lambda/N
            for page in outlink_dict:
                page_rank2[page] = lamb / len(outlink_dict)

            for page in outlink_dict:
                outlinks = outlink_dict[page]
                if len(outlinks) > 0:
                    distributed_rank = page_rank1[page]/len(outlinks)
                    for outlink in outlinks:
                        page_rank2[outlink] += (1 - lamb) * distributed_rank 
                else:
                    #distribute its rank to all the pages
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

    with open(inlinksFile, 'w') as file:
        inlink_dict = topFrequency(reverse_dict_list(outlink_dict), k)
        rank = 0
        for page, inlinkCount in inlink_dict:
            rank = rank + 1
            file.write(page)
            file.write("\t")
            file.write(str(rank))
            file.write("\t")
            file.write(str(inlinkCount))
            file.write("\n")
        
    with open(pagerankFile, 'w') as file:
        sortedPageRank = topFrequency(page_rank2, k)
        rank = 0
        for page, overallRank in sortedPageRank:
            rank = rank + 1
            file.write(page)
            file.write("\t")
            file.write(str(rank))
            file.write("\t")
            file.write(str(overallRank))
            file.write("\n")

if __name__ == '__main__':
        # Read arguments from command line; or use sane defaults for IDE.
        argv_len = len(sys.argv)
        inputFile = sys.argv[1] if argv_len >= 2 else "links-ireland.srt.gz"
        lambda_val = float(sys.argv[2]) if argv_len >=3 else 0.2
        tau = float(sys.argv[3]) if argv_len >=4 else 0.005
        inLinksFile = sys.argv[4] if argv_len >= 5 else "inlinks.txt"
        pagerankFile = sys.argv[5] if argv_len >= 6 else "pagerank.txt"
        k = int(sys.argv[6]) if argv_len >= 7 else 100
        main(inputFile, lambda_val, tau, inLinksFile, pagerankFile, k)