import math
import copy
import time

def sortItems(itemsList):
    """
    This function sorts the items in a descending order.

    Arguments: list[float]: List of item sizes

    Returns: list[float]: New list of items sorted in a descending order based on size.
    """
    return sorted(itemsList, reverse=True)

def placeItem(item, binIndex, usedBins, binRemainingCapacities):
    """
    This function places an item in a specific bin and updates its remaining capacity.

    Arguments:
        item (float): Size of the item to place.
        binIndex (int): Index of the target bin in usedBins.
        usedBins (list[list[float]]): Current items in each bin
        binRemainingCapacities (list[float]): Remaining capacity for each bin.

    Returns: None.
    """
    usedBins[binIndex].append(item)
    binRemainingCapacities[binIndex] -= item

def removeItem(item, binIndex, usedBins, binRemainingCapacities):
    """
    This function removes the last item from a specific bin and restores its remaining capacity.

    Arguments:
        item (float): Size of the item to remove.
        binIndex (int): Index of the bin in usedBins.
        usedBins (list[list[float]]): Current items in each bin.
        binRemainingCapacities (list[float]): Remaining capacity for each bin.

    Returns: None
    """
    removed = usedBins[binIndex].pop()
    binRemainingCapacities[binIndex] += removed


def calculateLowerBound(remainingItems, binCapacity):
    totalSize = sum(remainingItems)
    return math.ceil(totalSize / binCapacity)



def copyBins(bins):
    return copy.deepcopy(bins)
  


def pruneBranch(usedBins, bestSolution, remainingItems, binCapacity):
    print("Remaining items when calculating pruneBranch: ", remainingItems)
    lowerBound = calculateLowerBound(remainingItems, binCapacity)
    print("Lower bound : ", lowerBound)
    if len(usedBins) + lowerBound >= len(bestSolution):
        return True

    return False


def initializeSolution(items, binCapacity):
    bins = []
    for item in items:
        placed = False
        for b in bins:
            if sum(b) + item <= binCapacity:
                b.append(item)
                placed = True
                break
        if not placed:
            bins.append([item])
    return bins

    pass

def findFeasibleBins(item, binRemainingCapacities):
    """
    This function loops through the remaining space in binRemainingCapacities list to find the indices of bins where the given item still fits.

    Arguments: 
        item (float): Size of the item to place.
        binRemainingCapacities (list[float]): Remaining capacity for each bin.

    Returns: list[int]: Indices of bins where the item fits.
    """
    indices = []
    for i, remaining in enumerate(binRemainingCapacities):
        if item <= remaining:
            indices.append(i)
    return indices
