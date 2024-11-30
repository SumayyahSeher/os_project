def optimalPageReplace(frame, fsize, reference, index, totalReferences):
  
    farthest = -1
    pageToReplace = -1

    for i in range(fsize):
        nextUse = -1
        for j in range(index + 1, totalReferences):
            if frame[i] == reference[j]:
                nextUse = j
                break

        if nextUse == -1:
            return i

        if nextUse > farthest:
            farthest = nextUse
            pageToReplace = i

    return pageToReplace

def OptimalAlgorithm(frameSize, referenceString):
    frame = [-1] * frameSize 
    pageFaults = 0
    hits = 0
    misses = 0

    totalReferences = len(referenceString)

    for i in range(totalReferences):
        page = referenceString[i]
        pageFound = False

        if page in frame:
            pageFound = True
            hits += 1

        if not pageFound:
            misses += 1
            pageFaults += 1

            if -1 in frame:
                emptyIndex = frame.index(-1)
                frame[emptyIndex] = page
            else:
                pageToReplace = optimalPageReplace(frame, frameSize, referenceString, i, totalReferences)
                frame[pageToReplace] = page

    hitPer = (hits / totalReferences)*100
    missPer = (misses / totalReferences) *100

    return pageFaults, hits, misses, hitPer, missPer

def opt_main():
    f = int(input("Enter the number of frames: "))
    r = list(map(int, input("Enter the reference string (space-separated integers): ").split()))

    pageFaults, hits, misses, hitPer, missPer = OptimalAlgorithm(f, r)

    print(f"Page Faults: {pageFaults}")
    print(f"Hits: {hits}")
    print(f"Misses: {misses}")
    print(f"Hit Ratio: {hitPer:2f}%")
    print(f"Miss Ratio: {missPer:2f}%")

if __name__ == "__main__":
    opt_main()
