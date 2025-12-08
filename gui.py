import tkinter as tk
from tkinter import ttk, messagebox

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("1D Bin Packing Solver")
        self.root.geometry("1920x1080")
        self.binLabel = tk.Label(self.root, text="", font=("Courier", 16), justify="left", anchor="nw")
        self.binLabel.pack(fill="both", padx=20, pady=20)
    def drawBinFill(self,fillRate, binNumber):
        barlength = 20
        filled = int(fillRate*barlength)
        empty = barlength - filled
        bar = f"Bin {binNumber} : "
        bar += "|" + ("█"*filled) + ("-"*empty) + "| " + str(fillRate*100) + "%"
        currentText = self.binLabel["text"]
        newText = currentText + "\n" + bar
        self.binLabel.config(text=newText)
        self.root.update() 
        return bar

test = GUI()

# Container for all controls (instructions + inputs + dropdown)
topFrame = tk.Frame(test.root)
topFrame.pack(side="top", pady=20)

# Instructions
instructions = tk.Label(
    topFrame,
    text=("1D Bin Packing Solver\nEnter the minimum and maximum item sizes, then choose an algorithm to run.\nThe solver will pack items into bins of fixed capacity and show the bin usage."),
    font=("Helvetica", 14),
    justify="center")
instructions.pack(pady=10)

# Min/Max inputs
inputFrame = tk.Frame(topFrame)
inputFrame.pack(pady=10)

tk.Label(inputFrame, text="Min Item Size:").grid(row=0,column=0, padx=10)
entMinSize =tk.Entry(inputFrame, width=10)
entMinSize.grid(row=0, column=1,padx=10)
tk.Label(inputFrame, text="Max Item Size:").grid(row=0,column=2, padx=10)
entMaxSize = tk.Entry(inputFrame, width=10)
entMaxSize.grid(row=0, column=3,padx=10)

# Dropdown menu for algorithms
algoFrame = tk.Frame(topFrame)
algoFrame.pack(pady=10)
tk.Label(algoFrame,text="Select Algorithm:").pack()

# variable to hold selected algorithm
selectedAlgo = tk.StringVar(test.root)
selectedAlgo.set("Backtracking Algorithm")  # default
algoOptions = ["Backtracking Algorithm","Cultural Algorithm","Both"] # List of options

# remember last selection
lastSelection = {"value": selectedAlgo.get()}

def whenAlgoChange(choice):
    # choice is the new value selected from the dropdown
    if choice == lastSelection["value"]:
        return # the same option is selected again, nothing will change
    # update selection value
    lastSelection["value"] = choice
    selectedAlgo.set(choice)

algoDropdown = ttk.OptionMenu(
    algoFrame,
    selectedAlgo,
    selectedAlgo.get(), # default shown value
    *algoOptions,
    command=whenAlgoChange)
algoDropdown.pack(pady=5)

test.drawBinFill(0.81, 1)
test.drawBinFill(0.45, 2)
test.drawBinFill(1.0, 3)

test.root.mainloop()