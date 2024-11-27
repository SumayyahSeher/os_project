def lruAlgorithm(frameSize, referenceString):
    frame = []  # Memory frame to store pages
    pageFaults = 0
    hits = 0
    misses = 0

    totalReferences = len(referenceString)

    for page in referenceString:
        if page in frame:
            # Page hit
            hits += 1
            # Move the page to the most recently used position
            frame.remove(page)
            frame.append(page)
        else:
            # Page miss
            misses += 1
            pageFaults += 1
            if len(frame) == frameSize:
                # Remove the least recently used page
                frame.pop(0)
            frame.append(page)

    # Calculate hit and miss ratios
    hitPer = (hits / totalReferences) * 100
    missPer = (misses / totalReferences) * 100

    return pageFaults, hits, misses, hitPer, missPer


if __name__ == "__main__":
    # Input frame size and reference string
    f = int(input("Enter the number of frames: "))
    r = list(map(int, input("Enter the reference string (space-separated integers): ").split()))

    # Run the LRU algorithm
    pageFaults, hits, misses, hitPer, missPer = lruAlgorithm(f, r)

    # Display the results
    print(f"Page Faults: {pageFaults}")
    print(f"Hits: {hits}")
    print(f"Misses: {misses}")
    print(f"Hit Ratio: {hitPer:.2f}%")
    print(f"Miss Ratio: {missPer:.2f}%")
