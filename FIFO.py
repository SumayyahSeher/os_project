import numpy as np

def fifo(Pageframes, reference_string):
    pagefaults = 0
    Memory = []

    for page in reference_string:
        if page not in Memory:
            pagefaults += 1
            if len(Memory) < Pageframes:
                Memory.append(page)
            else:
                Memory.pop(0)
                Memory.append(page)

    hit_r = 1 - (pagefaults / len(reference_string))
    miss_r = 1 - hit_r

    return pagefaults, hit_r, miss_r

if __name__ == "__main__":
    try:
        Pageframes = int(input("Enter the size of the frame: "))
        reference_string = list(input("Enter the reference string: "))
        pagefaults, hit_r, miss_r = fifo(Pageframes, reference_string)
        print("Page Faults:", pagefaults)
        print("Hit Ratio:", hit_r)
        print("Miss Ratio:", miss_r)
    except ValueError:
        print("Invalid input!")
