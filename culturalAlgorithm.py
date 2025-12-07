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

binSize = 10
populationSize = 50

totalItems = {}
selectedIndividuals = []
beliefs = {"min-bin-fill":1,"top-5-items":[]}
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
        while individual.getFillRate(binSize) < beliefs["min-bin-fill"]:
            itemID = weightedPick(availableItems, beliefs["top-5-items"])
            if individual.addItem(itemID, totalItems[itemID], binSize):
                availableItems.remove(itemID)
            else:
                break
        newIndividuals.append(individual)
    return newIndividuals
childPopulation = []
p1 = Individual()
p2 = Individual()
p1.items = {"A": 3, "B": 4}
p2.items = {"C": 5, "D": 2}

def crossOver(parent1, parent2, childPopulation):
   
    child = Individual()
    used_ids = set()
    parent_order = [parent1.items, parent2.items]
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
    childPopulation.append(child)
    return child


def evaluateFitness(individual):
    fill = sum(individual.items.values())
    individual.fitness = fill / individual.binSize
    return individual.fitness


def mutate(individual):
    if not individual.items:
        return individual

    key = random.choice(list(individual.items.keys()))
    individual.items.pop(key)

    individual.fitness = -1
    return individual

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

