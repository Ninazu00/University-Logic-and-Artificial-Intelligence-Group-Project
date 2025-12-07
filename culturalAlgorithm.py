import random

class Individual:
    def __init__(self):
        self.fitness = -1
        self.items = {}
    def getFillRate(self,binSize):
        fillAmount = sum(self.items.values())
        return fillAmount/binSize
    def addItem(self,itemID,itemSize,binSize):
        if sum(self.items.values()) + itemSize <= binSize:
            self.items[itemID] = itemSize
            return True
        return False
    
def updateBeliefs(selectedIndividuals,beliefs):
    #Keeps count of how many each item appeared in a solution based on its key
    itemsAppearances = {}
    itemsAppearances = dict.fromkeys(totalItems.keys(),0)
    for key in itemsAppearances:
        for  ind in selectedIndividuals:
            if key in ind.items:
                itemsAppearances[key]+=1
    beliefs["top-5-items"] = sorted(itemsAppearances,key = itemsAppearances.get, reverse = True)[:5]
    minFill = min(value.getFillRate(binSize) for value in selectedIndividuals)
    beliefs["min-bin-fill"] = minFill

def weightedPick(choices, top5):
    weights = []
    for item in choices:
        if item in top5:
            weights.append(3)
        else:
            weights.append(1)
    return random.choices(choices, weights = weights, k = 1)[0]


def applyBeliefs(beliefs,totalItems):
    newIndividuals = []
    for i in range(1,populationSize//2):
        availableItems = list(totalItems.keys())
        individual = Individual()
        while individual.getFillRate(binSize) < beliefs["min-bin-fill"] and availableItems:
            itemID = weightedPick(availableItems, beliefs["top-5-items"])
            if individual.addItem(itemID, totalItems[itemID], binSize):
                availableItems.remove(itemID)
            else:
                break
        newIndividuals.append(individual)
    return newIndividuals

def mutate(individual,mutationRate):
    if not individual.items:
        return individual

    if random.random() < mutationRate:
        key = random.choice(list(individual.items.keys()))
        individual.items.pop(key)

    individual.fitness = -1
    return individual

def crossOver(parent1, parent2, childPopulation,mutationRate):
   
    def createChild(firstParent, secondParent):
        child = Individual()
        used_ids = set()
        parent_order = [firstParent.items, secondParent.items]
        turn = 0
        while True:
            current_parent = parent_order[turn]
            added = False
            for item_id, item_size in current_parent.items():
                if item_id in used_ids:
                    continue
                current_child_size = sum(child.items.values())
                if current_child_size + item_size <= binSize:
                    child.items[item_id] = item_size
                    used_ids.add(item_id)
                    added = True
                    break
            if not added:
                break
            turn = 1 - turn
        return child
    child1 = createChild(parent1, parent2)
    child2 = createChild(parent2, parent1)

    child1 = mutate(child1,mutationRate)
    child2 = mutate(child2,mutationRate)

    childPopulation.append(child1)
    childPopulation.append(child2)

    return child1, child2


def evaluateFitness(individual):
    fill = sum(individual.items.values())
    individual.fitness = fill / binSize
    return individual.fitness

def selectAccepted(population):
    for ind in population:
        if ind.fitness == -1:
            evaluateFitness(ind)

    sortedPop = sorted(population, key=lambda x: x.fitness, reverse=True)

    half = len(sortedPop) // 2
    selected = sortedPop[:half]
    return selected

def initializePopulation():
    population = []
    for _ in range(populationSize):
        individual = Individual()
        items_list = list(totalItems.items())
        random.shuffle(items_list)
        for item_id, item_size in items_list:
            individual.addItem(item_id, item_size, binSize)
        population.append(individual)
    return population

def generateNewGeneration(childPopulation, newPopulation):
    nextGen = []
    nextGen.extend(childPopulation)
    nextGen.extend(newPopulation)
    while len(nextGen) < populationSize:
        ind = Individual()
        items_list = list(totalItems.items())
        random.shuffle(items_list)
        for item_id, item_size in items_list:
            ind.addItem(item_id, item_size, binSize)
        nextGen.append(ind)
    if len(nextGen) > populationSize:
        nextGen = nextGen[:populationSize]
    return nextGen

def terminateCondition(generation, maxGenerations,population):
    for ind in population:
        if ind.fitness == -1:
            evaluateFitness(ind)
    bestFitness = max(ind.fitness for ind in population)
    return bestFitness >= 0.90 or generation >= maxGenerations

def initializeTotalItems(minSize,maxSize,numItems):
    items = {}
    for i in range(numItems):
        itemID = i
        itemSize = random.randint(minSize, maxSize)
        items[itemID] = itemSize
    return items

def generateBinCulturalAlgorithm(maxGenerations, populationSize, mutationRate, totalItems, binSize):
    generation = 0
    population = initializePopulation()
    beliefs = {"min-bin-fill":1,"top-5-items":[]}
    while not terminateCondition(generation, maxGenerations, population):
        selectedIndividuals = selectAccepted(population)
        updateBeliefs(selectedIndividuals, beliefs)
        newPopulation = applyBeliefs(beliefs, totalItems)
        childPopulation = []
        while len(childPopulation) < populationSize // 2:
            parent1, parent2 = random.sample(selectedIndividuals, 2)
            crossOver(parent1, parent2, childPopulation,mutationRate)
        population = generateNewGeneration(childPopulation, newPopulation)
        generation += 1
    bestIndividual = max(population, key=lambda x: x.fitness)
    return bestIndividual

#Important variable definitions
binSize = 10
populationSize = 50
mutationRate = 0.1
totalItems = {}
maxGenerations = 100

totalItems = initializeTotalItems(3,7,20)
bestBin = generateBinCulturalAlgorithm(maxGenerations, populationSize, mutationRate, totalItems, binSize)
print("Items in best bin:", bestBin.items)
print("Best bin fill rate:", bestBin.getFillRate(binSize))
binAmount = 0
while totalItems:
    for itemID in bestBin.items.keys():
        totalItems.pop(itemID, None)
    if not totalItems:
        break
    bestBin = generateBinCulturalAlgorithm(maxGenerations, populationSize, mutationRate, totalItems, binSize)
    binAmount += 1
    print("Items in best bin:", bestBin.items)
    print("Best bin fill rate:", bestBin.getFillRate(binSize))
print("Total number of bins used: ", binAmount)