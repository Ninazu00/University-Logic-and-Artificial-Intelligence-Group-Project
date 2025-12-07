import culturalAlgorithm
import time

#Backtracking testing
#Fine tuning variables for the cultural algorithm
populationSize = 50
mutationRate = 0.1
maxGenerations = 100
#Generates the list of items based on parameters given by the user
totalItems = culturalAlgorithm.initializeTotalItems(3,7,20)
#User inputted value for the bin size
binSize = 10
binAmount = 0
bestBin = culturalAlgorithm.Individual()
startTimeCA = time.time()
#Executes the cultural algorithm repetitively until all items are packed into bins.
while totalItems:
    for itemID in bestBin.items.keys():
        totalItems.pop(itemID, None)
    if not totalItems:
        break
    bestBin = culturalAlgorithm.generateBinCulturalAlgorithm(maxGenerations, populationSize, mutationRate, totalItems, binSize)
    binAmount += 1
    print("Items in bin:", bestBin.items.values())
    print("Fill rate:", bestBin.getFillRate(binSize))
#Calculates the time it took the cultural algorithm to run
elapsedTimeCA = time.time()- startTimeCA
print("Total number of bins used: ", binAmount)
print("Time elapsed: ", elapsedTimeCA)
