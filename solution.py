def parcours(l: list):
    l = sorted(l)
    startIdx = 0;
    while startIdx != len(l) and l[startIdx] < 0:
        startIdx += 1
    negativeIdx = startIdx - 1
    positiveIdx = startIdx

    reif = {};

    # Calculates the fastest choice between both avialable ones: going left or going right
    def eval(negativeIdx, positiveIdx, currentIdx):
        if (positiveIdx == len(l) and negativeIdx == -1):
            reif[(negativeIdx, positiveIdx, currentIdx)] = (0, None)
        elif not (negativeIdx, positiveIdx, currentIdx) in reif:
            remainingHouses = (negativeIdx + len(l) - positiveIdx + 1)
            if positiveIdx != len(l): # if there isn't any house to the right, we ignore the possibillity of going right by giving it an infinit cose
                positiveScore = abs(l[positiveIdx] - l[currentIdx]) * remainingHouses + reif[(negativeIdx, positiveIdx + 1, positiveIdx)][0]
            else:
                positiveScore = float("inf");
            if negativeIdx != -1: # same as above
                negativeScore = abs(l[negativeIdx] - l[currentIdx]) * remainingHouses + reif[(negativeIdx - 1, positiveIdx, negativeIdx)][0]
            else:
                negativeScore = float("inf");
            if positiveScore < negativeScore:
                reif[(negativeIdx, positiveIdx, currentIdx)] = (positiveScore, True) # note that we store the best choice, True means right
            else:
                reif[(negativeIdx, positiveIdx, currentIdx)] = (negativeScore, False) # and False means left
        return reif[(negativeIdx, positiveIdx, currentIdx)][0]

    # We fill the space of solutions from the arrival to the start.
    # A recursive implementation would probably stack overflow
    # This version also saves memory
    for i in range(-1, negativeIdx + 1):
        for j in range(len(l), positiveIdx - 1, -1):
            eval(i, j, i + 1)
            eval(i, j, j - 1)

    # We have to pick the best starting house: eihter at the left or right of 0
    if startIdx == len(l): # we apply the same impossible choice startegy than in eval
        positiveStart = float("inf")
    else:
        positiveStart = abs(l[positiveIdx]) * len(l) + eval(negativeIdx, positiveIdx + 1, positiveIdx)
    if startIdx == 0: # see above
        negativeStart = float("inf")
    else:
        negativeStart = abs(l[negativeIdx]) * len(l) + eval(negativeIdx - 1, positiveIdx, negativeIdx)

    results = []
    if positiveStart < negativeStart:
        currentIdx = positiveIdx
        positiveIdx += 1;
    else:
        currentIdx = negativeIdx;
        negativeIdx -= 1;
    results.append(l[currentIdx])

    # Now it's a simple matter of picking the best choice each step.
    while positiveIdx != len(l) or negativeIdx != -1:
        if (reif[negativeIdx, positiveIdx, currentIdx][1]):
            currentIdx = positiveIdx
            positiveIdx += 1
        else:
            currentIdx = negativeIdx;
            negativeIdx -= 1;
        results.append(l[currentIdx])
    return results
