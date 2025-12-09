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
    This function removes an item from a specific bin and restores its remaining capacity.

    Arguments:
        item (float): Size of the item to remove.
        binIndex (int): Index of the bin in usedBins.
        usedBins (list[list[float]]): Current items in each bin.
        binRemainingCapacities (list[float]): Remaining capacity for each bin.

    Returns: None
    """
    usedBins[binIndex].remove(item)
    binRemainingCapacities[binIndex] += item

def calculateLowerBound(remainingItems, binCapacity):

    totalSize = sum(remainingItems)
    return math.ceil(totalSize / binCapacity)



def copyBins(bins):
    return copy.deepcopy(bins)
  


def pruneBranch(usedBins, bestSolution, remainingItems, binCapacity):
    lowerBound = calculateLowerBound(remainingItems, binCapacity)
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

def backtrack(currentIndex, usedBins, binRemainingCapacities, binCapacity, bestSolution, sortedItemsList):
    """
    This function contains the main backtracking algorithm logic, it performs a recursive backtracking search to minimize the number of bins.

    At each step, the function tries all feasible placements for the current
    item, including opening a new bin, and updates bestSolution when a better
    complete packing is found.

    Arguments: 
        currentIndex (int): Index of the next item to place in sortedItemsList.
        usedBins (list[list[float]]): The bins built so far during the search, each inner list holds the items in that bin.
        binRemainingCapacities (list[float]): Remaining capacity in each bin
        binCapacity (float): Capacity of a single bin.
        bestSolution (list[list[float]]): Best complete solution found so far.
        sortedItemsList (list[float]): Items sorted in a descending order.

    Returns: None.
    """
    # Base case: all items have been placed
    if currentIndex == len(sortedItemsList):
        if len(usedBins) < len(bestSolution):
            bestSolution.clear()
            bestSolution.extend(copyBins(usedBins))
        return

    item = sortedItemsList[currentIndex]

    # Remaining items (including current item) for lower bound pruning
    remainingItems = sortedItemsList[currentIndex:]
    if pruneBranch(usedBins, bestSolution, remainingItems, binCapacity):
        return

    # Try placing in existing bins (all feasible choices)
    feasibleBins = findFeasibleBins(item, binRemainingCapacities)
    for i in feasibleBins:
        placeItem(item, i, usedBins, binRemainingCapacities)
        backtrack(currentIndex + 1, usedBins, binRemainingCapacities,
                  binCapacity, bestSolution, sortedItemsList)
        removeItem(item, i, usedBins, binRemainingCapacities)

    # Try placing in a new bin
    usedBins.append([item])
    binRemainingCapacities.append(binCapacity - item)
    backtrack(currentIndex + 1, usedBins, binRemainingCapacities, binCapacity, bestSolution, sortedItemsList)
    usedBins.pop()
    binRemainingCapacities.pop()


def solveBinPacking(items, binCapacity):
    sortedItems = sortItems(items)
    bestSolution = initializeSolution(sortedItems, binCapacity)
    usedBins = []
    binRemainingCapacities = []
    start = time.time()
    backtrack(0, usedBins, binRemainingCapacities,
              binCapacity, bestSolution, sortedItems)
    execTime = time.time() - start
    return bestSolution, execTime