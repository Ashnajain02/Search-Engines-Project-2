
Breakdown - If it is not blatantly obvious (to a human who is not you), please indicate where in your source code the PageRank algorithm exists.
Description - Provide a description of system, design tradeoffs, etc., that you made. Focus on how you implemented the the loop and checked for convergence.
Libraries - List the software libraries you used, and for what purpose. Implementation must be your own work. If you are thinking of using any other libraries for this assignment, please send us an email to check first.
Dependencies - Provide instructions for downloading dependencies of the code. Not expecting anything here.
Building - Provide instructions for building the code.
Running - Provide instructions for running the code.

Breakdown:
    -the PageRank alorithm exists in pagerank.py file

Description:
    INITALIZATION:
        -I create a outlink_dict that stores pages as the keys, and the websites that they have links to as the value. This could be empty, if no outlinks exist. 
        -I create page_rank1 dict that it initalized with 1/N
        -I create page_rank2 dict that is initalized with lambda/N
        -convered = False
    WHILE NOT CONVERGED:
        -check for convergence -> if false then
        -reset the values of page_rank2 to lambda/N
        -get the outlinks of the page
        -if the page has no outlinks, then distribute to ALL the pages
        -if it has outlink, distribute to just those pages(s)
        -check convergence using L2 Norm. If the sum was < tau, then we know we have converged, and I set converged to True 
        -update page_rank1 value to page_rank2 
    Design Tradeoffs:
        -When ranking the website by inlink count, I had to reverse the outlink dictionary that I had created.
        -In a large dataset this could be a very expensive operation, and require a lot of time.
    
Libraries:
    -gzip: used to read into .gzip file
    -math: used to calculate L2 Norm to see if page_rank had converged
    -collections import Counter: used to rank the top page_rank and pages with most inlinks
    -sys: used to read inputs from the terminal

Dependencies: 
    -None

Building + Running:
    -using terminal enter the specifications, otherwise it will defualt to 
    -inputFile: link.srt.gz
    -lambda: 0.2
    -tau: 0.005
    -inlinksFile: inlinks.txt
    -pagerankFile: pagerank.txt
    -k: 100