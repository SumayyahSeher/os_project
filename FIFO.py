import numpy as np

def fifoAlgorithm(Pageframes, reference_string):
    pagefaults = 0
    Memory = []
    hits = 0
    misses = 0

    for page in reference_string:
        if page not in Memory:
            pagefaults += 1
            if len(Memory) < Pageframes:
                Memory.append(page)
                hits += 1  # Increment hits when a page is added to an empty frame
            else:
                misses += 1
                Memory.pop(0)
                Memory.append(page)

    hit_r = 1 - (pagefaults / len(reference_string))  
    miss_r = 1 - hit_r 

    # The function should return 5 values as expected by fifo_main
    return pagefaults, hits, misses, hit_r, miss_r
   
def fifo_main(): 

    Pageframes = int(input("Enter the size of the frame: "))
    reference_string = list(input("Enter the reference string: "))
    pagefaults, hits, misses, hit_r, miss_r = fifoAlgorithm(Pageframes, reference_string) 
    print("Page Faults:", pagefaults)
    print(f"Hits: {hits}")
    print(f"Misses: {misses}")
    print("Hit Ratio:", hit_r)
    print("Miss Ratio:", miss_r)
