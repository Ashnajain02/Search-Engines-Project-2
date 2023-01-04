#Ashna Jain
#Search Engines Project 2
#PageRank

import gzip
import math
from collections import Counter

with gzip.open('small.srt.gz', 'rb') as f:        
    converged = False
    lambdaa = 0.20
    tau = 0.005
    outlink_dict = {}
    website_encoding = {}
    page_rank1 = {}
    page_rank2 = {}
    file_content = f.read()
    file_content = file_content.split()
    print("file_content: ",file_content)

    #create a dictionary where each website string (key) has its own unique number (value)
    num = 0
    for i in range(len(file_content)):
        if file_content[i] not in website_encoding:
            website_encoding[file_content[i]] = num
            num = num + 1
    print("website_encoding: ",website_encoding)

    #iterate through website_encoding dict and page_rank to base value
    #these will be updated later
    for website in website_encoding:
        key = website_encoding.get(website)
        page_rank1[key] = 1/len(website_encoding)
    print("page_rank1: ",page_rank1)

    #go through file, and if a website is not already in dict, add it add the website it is point it to
    #its its already in the dict, then only add the website it points to 
    #Also set the value of page_rank2 to lambdaa/N
    i = 0
    while(i < len(file_content) - 1):
        key = website_encoding.get(file_content[i])
        value = website_encoding.get(file_content[i+1])
        if key not in outlink_dict:
            outlink_dict[key] = set()
            page_rank2[key] = lambdaa/len(website_encoding)
            #outlink_dict[key].add(value)
        if value not in outlink_dict:
            outlink_dict[value] = set()
            page_rank2[value] = lambdaa/len(website_encoding)
        #elif key in outlink_dict:
        outlink_dict[key].add(value)
        i = i + 2
    
    print("page_rank2: ", page_rank2)
    print("outlink_dict: ", outlink_dict)

    count = 0
    while converged == False:
    #while count < 4:
        #go through all the outlink of a page, and distribute the page's rank to it
        for website in page_rank2:
            page_rank2[website] = lambdaa/len(website_encoding)
            #print("page_rank2 while loop: ", page_rank2)

        #for each page
        for page in outlink_dict:
            #values = all the page's outlinks
            outlinks = outlink_dict.get(page)
            print("outlinks: ", outlinks)
            #if a page has zero outlinks
            if len(outlinks) == 0:
                #distributed rank is the page's rank divided by the total number of pages
                distributed_rank = page_rank1.get(page)/len(website_encoding)
                print("distributed_rank: ", distributed_rank)
                #for all the websites in page_rank
                for website in page_rank1:
                    #if the website is not the current page
                    if website != page:
                        #distribute the rank to the webside
                        page_rank2[website] = page_rank2.get(website) + ((1 - lambdaa) *  distributed_rank)
            else:
                distributed_rank = page_rank1.get(page)/len(outlinks)
                print("distributed_rank non empty: ", distributed_rank)
                for website in outlinks:
                    #print("page_rank2.get(website) BEFORE: ", page_rank2.get(website))
                    page_rank2[website] = page_rank2.get(website) + ((1 - lambdaa) * distributed_rank)
                    #print("page_rank2.get(website) AFTER: ", page_rank2.get(website))
        sum = 0
        for i in range(len(page_rank1)):
            sum = sum + math.pow(page_rank1.get(i) - page_rank2.get(i), 2)
        sum = math.sqrt(sum)
        print("sum: ", sum)
        if sum < tau:
            converged = True
        #count = count + 1
        for page in page_rank2:
                page_rank1[page] = page_rank2[page]
        print(page_rank1)

def reverse_dict_list(d):
    reversed = {}
    for key, values in d.items():
        for v in values:
            reversed.setdefault(v, 0)
            reversed.setdefault(key, 0)
            reversed[v] = reversed.get(v) + 1
    return reversed  # fix this line!

def reverse_encoding(d):
    reversed = {}
    for key, value in d.items():
        reversed[value] = key
    return reversed  # fix this line!

print(reverse_encoding(website_encoding))

def topFrequency(data):
    dict = Counter(data)
    top = dict.most_common()  
    return top

with open(r'inlinks.txt', 'w') as file:
    #file.write(data)
    rank = 0
    rev_website_encodings = reverse_encoding(website_encoding)
    for x in topFrequency(reverse_dict_list(outlink_dict)):
        rank = rank + 1
        website = rev_website_encodings.get(x[0])
        inLinkCount = x[1]
        file.write(website.decode("utf-8"))
        file.write("\t")
        file.write(str(rank))
        file.write("\t")
        file.write(str(inLinkCount))
        file.write("\n")
#////////////////////////

    