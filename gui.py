import tkinter as tk
import time
import culturalAlgorithm
import backtrackingAlgorithm
from tkinter import ttk

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("1D Bin Packing Solver")
        self.root.geometry("1920x1080")
        #Graph frame
        self.binGraphFrame = tk.Frame(self.root)
        #Left graph for backtracking
        self.leftFrame = tk.Frame(self.binGraphFrame)
        self.leftFrame.pack(side="left", padx=20)
        self.leftLabel =  tk.Label(self.leftFrame, text="Backtracking algorithm result", font=("Courier", 16))
        self.leftLabel.pack()
        self.binGraphLeft = tk.Text(self.leftFrame, font=("Courier", 16), width=45)
        self.binGraphLeft.pack(padx=20, pady=20)
        #Right graph for cultural algorithm
        self.rightFrame = tk.Frame(self.binGraphFrame)
        self.rightFrame.pack(side="left", padx=20)
        self.rightLabel = tk.Label(self.rightFrame, text="Cultural algorithm result", font=("Courier", 16))
        self.rightLabel.pack()
        self.binGraphRight = tk.Text(self.rightFrame, font=("Courier", 16), width=45)
        self.binGraphRight.pack(padx=20, pady=20)

        # Container for all controls (instructions + inputs + dropdown)
        self.topFrame = tk.Frame(self.root)
        self.topFrame.pack(side="top", pady=20)
        #Container for all algorithm graphs
        self.binGraphFrame.pack(expand=True)
        # Instructions
        self.instructions = tk.Label(
            self.topFrame,
            text=("1D Bin Packing Solver\nEnter the minimum and maximum item sizes, then choose an algorithm to run.\nThe solver will pack items into bins of fixed capacity and show the bin usage."),
            font=("Helvetica", 14),
            justify="center")
        self.instructions.pack(pady=10)

        # Inputs
        self.inputFrame = tk.Frame(self.topFrame)
        self.inputFrame.pack(pady=10)

        tk.Label(self.inputFrame, text="Min Item Size:").grid(row=0,column=0, padx=10)
        self.entMinSize = tk.Entry(self.inputFrame, width=10)
        self.entMinSize.grid(row=0, column=1,padx=10)
        tk.Label(self.inputFrame, text="Max Item Size:").grid(row=0,column=2, padx=10)
        self.entMaxSize = tk.Entry(self.inputFrame, width=10)
        self.entMaxSize.grid(row=0, column=3,padx=10)
        tk.Label(self.inputFrame, text="Number of Items:").grid(row=0, column=4, padx=10)
        self.itemNumber = tk.Entry(self.inputFrame, width=10)
        self.itemNumber.grid(row=0, column=5, padx=10)
        tk.Label(self.inputFrame, text="Bin Capacity:").grid(row=0, column=6, padx=10)
        self.binCapacity = tk.Entry(self.inputFrame, width=10)
        self.binCapacity.grid(row=0, column=7, padx=10)
        # Dropdown menu for algorithms
        self.algoFrame = tk.Frame(self.topFrame)
        self.algoFrame.pack(pady=10)
        tk.Label(self.algoFrame,text="Select Algorithm:").pack()

        # variable to hold selected algorithm
        self.selectedAlgo = tk.StringVar(self.root)
        self.selectedAlgo.set("Backtracking Algorithm") # default
        self.algoOptions = ["Backtracking Algorithm","Cultural Algorithm","Both"] # List of options

        # remember last selection
        self.lastSelection = {"value": self.selectedAlgo.get()}

        self.algoDropdown = ttk.OptionMenu(
            self.algoFrame,
            self.selectedAlgo,
            self.selectedAlgo.get(), # default shown value
            *self.algoOptions,
            command=self.whenAlgoChange)
        self.algoDropdown.pack(pady=5)

        self.runButton = tk.Button(self.topFrame, text="Run", font=("Helvetica", 14), command=self.runAlgorithm)
        self.runButton.pack(pady=20)

        self.btTimeLabel = tk.Label(self.leftFrame, text="Backtracking time: 0 S")
        self.btTimeLabel.pack()
        self.btBinsLabel = tk.Label(self.leftFrame, text="Backtracking bins: 0")
        self.btBinsLabel.pack()

        self.caTimeLabel = tk.Label(self.rightFrame, text="Cultural Algorithm time: 0 S")
        self.caTimeLabel.pack()
        self.caBinsLabel = tk.Label(self.rightFrame, text="Cultural Algorithm bins: 0")
        self.caBinsLabel.pack()
    
    def whenAlgoChange(self, choice):
        # choice is the new value selected from the dropdown
        if choice == self.lastSelection["value"]:
            return # the same option is selected again, nothing will change
        # update selection value
        self.lastSelection["value"] = choice
        self.selectedAlgo.set(choice)

    def drawBinFillRight(self,fillRate, binNumber):
        barlength = 20
        filled = int(fillRate*barlength)
        empty = barlength - filled
        bar = f"Bin {binNumber} : "
        bar += "|" + ("█"*filled) + ("-"*empty) + "| " + str(fillRate*100) + "%"
        newText = "\n" + bar
        self.binGraphRight.config(state="normal")
        self.binGraphRight.insert("end", newText + "\n")
        self.binGraphRight.config(state="disabled")
        self.binGraphRight.see("end")
        return bar
    
    def drawBinFillLeft(self, bestSolution):
        maxBinSum = max(sum(binItems) for binItems in bestSolution)
        for binNumber, binItems in enumerate(bestSolution, start=1):
            binCapacityUsed = sum(binItems)
            barlength = 20
            fillRate = binCapacityUsed / maxBinSum 
            filled = int(fillRate * barlength)
            empty = barlength - filled
            bar = f"Bin {binNumber} : "
            bar += "|" + ("█"*filled) + ("-"*empty) + "| " + f"{(binCapacityUsed / maxBinSum)*100:.1f}%"
            self.binGraphLeft.insert("end", bar + "\n" + "\n")        
        self.binGraphLeft.config(state="disabled")
        self.binGraphLeft.see("end")

    def runAlgorithm(self):
        minSize = int(self.entMinSize.get())
        maxSize = int(self.entMaxSize.get())
        numItems = int(self.itemNumber.get())
        binSize = int(self.binCapacity.get())
        choice =  self.selectedAlgo.get()
        items = culturalAlgorithm.initializeTotalItems(minSize, maxSize, numItems)
        itemsCA = items.copy()
        sizes = list(items.values())

        if choice == "Backtracking Algorithm":
            bestSolutionBT, execTimeBT = backtrackingAlgorithm.solveBinPacking(sizes, binSize)
            startTimeBT = time.time()
            self.drawBinFillLeft(bestSolutionBT)
            elapsedTimeBT = time.time()- startTimeBT
            print("Time elapsed for Backtracking: ", elapsedTimeBT)
            self.btTimeLabel.config(text=f"Backtracking time: {execTimeBT:.7f} S")
            self.btBinsLabel.config(text=f"Backtracking bins: {len(bestSolutionBT)}")

        elif choice == "Cultural Algorithm":
            #Fine tuning variables for the cultural algorithm
            populationSize = 20
            mutationRate = 0.15
            maxGenerations = 100
            #Needed values to be passed
            bestBin = culturalAlgorithm.Individual()
            #Starting time before running the cultural algorithm
            startTimeCA = time.time()
            #Calls the cultural algorithm
            binAmountCA = culturalAlgorithm.culturalAlgorithmFullSolve(populationSize,mutationRate,maxGenerations,itemsCA,binSize,bestBin,self)
            #Calculates the time it took the cultural algorithm to run
            elapsedTimeCA = time.time()- startTimeCA
            print("Time elapsed: ", elapsedTimeCA) 
            self.caTimeLabel.config(text=f"Cultural Algorithm time: {elapsedTimeCA:.2f} S")
            self.caBinsLabel.config(text=f"Cultural Algorithm bins: {binAmountCA}")
        else:  
            bestSolutionBT, execTimeBT = backtrackingAlgorithm.solveBinPacking(sizes, binSize)
            startTimeBT = time.time()
            self.drawBinFillLeft(bestSolutionBT)
            elapsedTimeBT = time.time()- startTimeBT
            self.btTimeLabel.config(text=f"Backtracking time: {elapsedTimeBT:.7f} S")
            self.btBinsLabel.config(text=f"Backtracking bins: {len(bestSolutionBT)}")
            #Cultural Algorithm Run
            #Fine tuning variables for the cultural algorithm
            populationSize = 20
            mutationRate = 0.15
            maxGenerations = 100
            #Needed values to be passed
            bestBin = culturalAlgorithm.Individual()
            #Starting time before running the cultural algorithm
            startTimeCA = time.time()
            #Calls the cultural algorithm
            binAmountCA = culturalAlgorithm.culturalAlgorithmFullSolve(populationSize,mutationRate,maxGenerations,itemsCA,binSize,bestBin,self)
            #Calculates the time it took the cultural algorithm to run
            elapsedTimeCA = time.time()- startTimeCA
            print("Time elapsed for Cultural: ", elapsedTimeCA) 
            print("Time elapsed for Backtracking: ", elapsedTimeBT)
            self.caTimeLabel.config(text=f"Cultural Algorithm time: {elapsedTimeCA:.2f} S")
            self.caBinsLabel.config(text=f"Cultural Algorithm bins: {binAmountCA}")