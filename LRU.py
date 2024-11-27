def lruAlgorithm(frameSize, referenceString):
    frame = []
    pageFaults = 0
    hits = 0
    misses = 0
    totalReferences = len(referenceString)
    for page in referenceString:
        if page in frame:
            hits += 1
            frame.remove(page)
            frame.append(page)
        else:
            misses += 1
            pageFaults += 1
            if len(frame) == frameSize:
                frame.pop(0)
            frame.append(page)
    hitPer = (hits / totalReferences) * 100
    missPer = (misses / totalReferences) * 100
    return pageFaults, hits, misses, hitPer, missPer
if __name__ == "__main__":
    f = int(input("Enter the number of frames: "))
    r = list(map(int, input("Enter the reference string (space-separated integers): ").split()))
    pageFaults, hits, misses, hitPer, missPer = lruAlgorithm(f, r)
    print(f"Page Faults: {pageFaults}")
    print(f"Hits: {hits}")
    print(f"Misses: {misses}")
    print(f"Hit Ratio: {hitPer:.2f}%")
    print(f"Miss Ratio: {missPer:.2f}%")
