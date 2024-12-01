import numpy as np
def fifoAlgorithm(Pageframes, reference_string):
    pagefaults = 0
    Memory = []
    hits = 0

    for page in reference_string:
        if page in Memory:
            hits += 1  # Page is already in memory, increment hits
        else:
            pagefaults += 1  # Page fault occurs when page is not in memory
            if len(Memory) < Pageframes:
                Memory.append(page)
            else:
                Memory.pop(0)  # Remove the oldest page
                Memory.append(page)

    misses = pagefaults
    hit_r = hits / len(reference_string)
    miss_r = 1 - hit_r

    return pagefaults, hits, misses, hit_r, miss_r

def fifo_main():
    Pageframes = int(input("Enter the size of the frame: "))
    reference_string = list(input("Enter the reference string (space-separated): ").split())
    pagefaults, hits, misses, hit_r, miss_r = fifoAlgorithm(Pageframes, reference_string)
    print("Page Faults:", pagefaults)
    print("Hits:", hits)
    print("Misses:", misses)
    print("Hit Ratio:", round(hit_r, 2))
    print("Miss Ratio:", round(miss_r, 2))
