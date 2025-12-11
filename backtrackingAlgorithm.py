import math
import copy
import time
import utils

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
    print("Remaining items when calculating backtrack: ", sortedItemsList)
    # Base case: all items have been placed
    if currentIndex == len(sortedItemsList):
        if len(usedBins) < len(bestSolution):
            bestSolution.clear()
            bestSolution.extend(utils.copyBins(usedBins))
        return

    item = sortedItemsList[currentIndex]

    # Remaining items (including current item) for lower bound pruning
    remainingItems = sortedItemsList[currentIndex:]
    if utils.pruneBranch(usedBins, bestSolution, remainingItems, binCapacity):
        return

    # Try placing in existing bins (all feasible choices)
    feasibleBins = utils.findFeasibleBins(item, binRemainingCapacities)
    for i in feasibleBins:
        utils.placeItem(item, i, usedBins, binRemainingCapacities)
        backtrack(currentIndex + 1, usedBins, binRemainingCapacities,
                  binCapacity, bestSolution, sortedItemsList)
        utils.removeItem(item, i, usedBins, binRemainingCapacities)

    # Try placing in a new bin
    usedBins.append([item])
    binRemainingCapacities.append(binCapacity - item)
    backtrack(currentIndex + 1, usedBins, binRemainingCapacities, binCapacity, bestSolution, sortedItemsList)
    usedBins.pop()
    binRemainingCapacities.pop()


def solveBinPacking(items, binCapacity):
    print("Items to solve with: ", items)
    sortedItems = utils.sortItems(items)
    bestSolution = utils.initializeSolution(sortedItems, binCapacity)
    usedBins = []
    binRemainingCapacities = []
    start = time.time()
    backtrack(0, usedBins, binRemainingCapacities,
              binCapacity, bestSolution, sortedItems)
    execTime = time.time() - start
    return bestSolution, execTime