import tkinter as tk
from tkinter import ttk, messagebox

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("1D Bin Packing Solver")
        self.root.geometry("1920x1080")
        #Graph frame
        self.binGraphFrame = tk.Frame(self.root)
        self.binGraphFrame.pack(expand=True)
        #Left graph for backtracking
        self.leftFrame = tk.Frame(self.binGraphFrame)
        self.leftFrame.pack(side="left", padx=20)
        self.binGraphLeft = tk.Text(self.leftFrame, font=("Courier", 16),width=45)
        self.binGraphLeft.pack(side="left",padx=20, pady=20)
        self.leftLabel = tk.Label(self.leftFrame, text="Algorithm 1", font=("Courier", 16))
        #Right graph for cultural algorithm
        self.rightFrame = tk.Frame(self.binGraphFrame)
        self.rightFrame.pack(side="left", padx=20)
        self.rightLabel = tk.Label(self.rightFrame, text="Algorithm 2", font=("Arial", 16))
        self.binGraphRight = tk.Text(self.binGraphFrame, font=("Courier", 16),width=45)
        self.binGraphRight.pack(side="left",padx=20, pady=20)

        # Container for all controls (instructions + inputs + dropdown)
        self.topFrame = tk.Frame(self.root)
        self.topFrame.pack(side="top", pady=20)

        # Instructions
        self.instructions = tk.Label(
            self.topFrame,
            text=("1D Bin Packing Solver\nEnter the minimum and maximum item sizes, then choose an algorithm to run.\nThe solver will pack items into bins of fixed capacity and show the bin usage."),
            font=("Helvetica", 14),
            justify="center")
        self.instructions.pack(pady=10)

        # Min/Max inputs
        self.inputFrame = tk.Frame(self.topFrame)
        self.inputFrame.pack(pady=10)

        tk.Label(self.inputFrame, text="Min Item Size:").grid(row=0,column=0, padx=10)
        self.entMinSize = tk.Entry(self.inputFrame, width=10)
        self.entMinSize.grid(row=0, column=1,padx=10)
        tk.Label(self.inputFrame, text="Max Item Size:").grid(row=0,column=2, padx=10)
        self.entMaxSize = tk.Entry(self.inputFrame, width=10)
        self.entMaxSize.grid(row=0, column=3,padx=10)

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
    
    def whenAlgoChange(self, choice):
        # choice is the new value selected from the dropdown
        if choice == self.lastSelection["value"]:
            return # the same option is selected again, nothing will change
        # update selection value
        self.lastSelection["value"] = choice
        self.selectedAlgo.set(choice)

    def drawBinFillLeft(self,fillRate, binNumber):
        barlength = 20
        filled = int(fillRate*barlength)
        empty = barlength - filled
        bar = f"Bin {binNumber} : "
        bar += "|" + ("█"*filled) + ("-"*empty) + "| " + str(fillRate*100) + "%"
        newText = "\n" + bar
        self.binGraphLeft.config(state="normal")
        self.binGraphLeft.insert("end", newText + "\n")
        self.binGraphLeft.config(state="disabled")
        self.binGraphLeft.see("end")
        return bar
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

test = GUI()

test.root.mainloop()