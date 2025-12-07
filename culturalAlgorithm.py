
class Individual:
    def __init__(self,binSize):
        self.fitness = -1
        self.items = {}
        self.binSize = binSize
    def getFillRate(self):
        fillAmount = sum(self.items.values())
        return fillAmount/self.binSize

totalItems = {}
selectedIndividuals = []
beliefs = {"min-bin-fill":0,"top-5-items":[]}
def updateBeliefs(selectedIndividuals,beliefs):
    #Keeps count of how many each item appeared in a solution based on its key
    itemsAppearances = {}
    itemsAppearances = dict.fromkeys(totalItems.keys(),0)
    for key in itemsAppearances:
        for  ind in selectedIndividuals:
            if key in ind.items:
                itemsAppearances[key]+=1
    beliefs["top-5-items"] = sorted(itemsAppearances,key = itemsAppearances.get, reverse = True)[:5]
    minFill = min(value.getFillRate() for value in selectedIndividuals)


childPopulation = []
p1 = Individual(binSize)
p2 = Individual(binSize)
p1.items = {"A": 10, "B": 20}
p2.items = {"C": 15, "D": 5}

def crossOver(parent1, parent2, childPopulation):
   
    child = Individual(parent1.binSize)
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
            if current_child_size + item_size <= child.binSize:
                child.items[item_id] = item_size
                used_ids.add(item_id)
                added = True
                break
        if not added:
            break
        turn = 1 - turn
    childPopulation.append(child)
    return child


