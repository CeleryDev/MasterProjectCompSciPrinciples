"""
Fitness Table Gui
BENJAMIN FEIBUS
AP COMP SCI PRIN
5th PERIOD
CMDR SCHENK
APR 19 2023
"""

import tkinter as tk
from tkinter import ttk
from FitnessCRUD import mySQLFunctions as sql

class FitnessGUI:

    def __init__(self):

        self.currentRecordDay = 0
        self.currentRecordFood = 0
        self.holdRecordDay = (0, "", 0, 0, 0, 0, 0)
        self.holdRecordFood = (0, 0, "", 0, 0, 0, 0, 0)
        self.midInsert = False
        self.answer = ""

        self.sql = sql()

        self.mainWin = tk.Tk()
        self.mainWin.title("Fitness Data Tracking GUI V1.0")

        self.notebook = ttk.Notebook(self.mainWin)
        self.notebook.pack(pady=10, expand=True)

        self.menuBarFood = tk.Menu(self.mainWin)
        self.menuBarMain = tk.Menu(self.mainWin)
        self.connectMenu = tk.Menu(self.menuBarMain, tearoff=0)
        self.connectMenu.add_command(label='Connect', command=self.connectionManager)
        self.connectMenu.add_command(label="Disconnect", command=self.connectionManager)
        self.connectMenu.add_command(label="Exit", command=self.mainWin.destroy)
        self.menuBarMain.add_cascade(label="File", menu=self.connectMenu)

        self.recordMenuFood = tk.Menu(self.menuBarFood, tearoff=0)
        self.recordMenuFood.add_command(label="New Food", command=lambda:self.insertFood())
        self.recordMenuFood.add_command(label="Save Food", command=self.saveChangedFood)
        self.recordMenuFood.add_command(label="Delete Current Food", command=self.showConfirmAlertFood)
        self.menuBarFood.add_cascade(label="Records", menu=self.recordMenuFood)

        self.navMenuFood = tk.Menu(self.menuBarFood, tearoff=0)
        self.navMenuFood.add_command(label="First Food", command= lambda: [self.setToZero(), self.showRecordFood(0)])
        self.navMenuFood.add_command(label="Previous Food", command= lambda:self.jumpRecFood(-1))
        self.navMenuFood.add_command(label="Next Food", command= lambda: self.jumpRecFood(1))
        self.navMenuFood.add_command(label="Last Food", command= lambda: self.jumpRecFood(len(self.sql.recordsFood)-1))
        self.menuBarFood.add_cascade(label="Navigate", menu=self.navMenuFood)

        self.helpMenu = tk.Menu(self.menuBarMain, tearoff=0)
        self.helpMenu.add_command(label="About", command=self.showAboutAlert)
        self.menuBarMain.add_cascade(label="Help", menu=self.helpMenu)

        self.mainWin.config(menu=self.menuBarFood)

        self.frameFood = tk.Frame(self.notebook, width = 1000, height= 1000)

        
        self.connectButton = tk.Button(self.frameFood, text="Connect", width=10, height=2, bg="gray", fg="black", command=self.connectionManager)
        self.connectButton.place(x=100, y=100)
        
        self.lblFoodDay = tk.Label(self.frameFood, text="Day Key")
        self.foodDayEntry = tk.Entry(self.frameFood, bd=3, relief="sunken")
        self.lblFoodName = tk.Label(self.frameFood, text="Food Name")
        self.foodNameEntry = tk.Entry(self.frameFood, bd=3, relief="sunken")
        self.lblFoodCal = tk.Label(self.frameFood, text="Calories")
        self.foodCalEntry = tk.Entry(self.frameFood, bd=3, relief="sunken")
        self.lblFoodProtein = tk.Label(self.frameFood, text="Protein")
        self.foodProteinEntry = tk.Entry(self.frameFood, bd=3, relief="sunken")
        self.lblFoodFiber = tk.Label(self.frameFood, text="Fiber")
        self.foodFiberEntry = tk.Entry(self.frameFood, bd=3, relief="sunken")
        self.lblFoodCarb = tk.Label(self.frameFood, text="Carbs")
        self.foodCarbEntry = tk.Entry(self.frameFood, bd=3, relief="sunken")
        self.lblFoodFat = tk.Label(self.frameFood, text="Fat")
        self.foodFatEntry = tk.Entry(self.frameFood, bd=3, relief="sunken")

        self.lblFoodDay.place(x=100, y=150)
        self.foodDayEntry.place(x=200, y=150)
        self.lblFoodName.place(x=100, y=200)
        self.foodNameEntry.place(x=200, y=200)
        self.lblFoodCal.place(x=100, y=250)
        self.foodCalEntry.place(x=200, y=250)
        self.lblFoodProtein.place(x=100, y=300)
        self.foodProteinEntry.place(x=200, y=300)
        self.lblFoodFiber.place(x=100, y=350)
        self.foodFiberEntry.place(x=200, y=350)
        self.lblFoodCarb.place(x=100, y=400)
        self.foodCarbEntry.place(x=200, y=400)
        self.lblFoodFat.place(x=100, y=450)
        self.foodFatEntry.place(x=200, y=450)

        self.btnStartFood = tk.Button(self.frameFood, text="|<", width=10, height=2, bg="gray", fg="black", command=lambda: [self.setToZero(), self.showRecordFood(0)])
        self.btnPrevFood = tk.Button(self.frameFood, text="<", width=10, height=2, bg="gray", fg="black", command=lambda: self.jumpRecFood(-1))
        self.btnRewindFood = tk.Button(self.frameFood, text="<<", width=10, height=2, bg="gray", fg="black", command=lambda: self.jumpRecFood(-5))
        self.btnFastForwardFood = tk.Button(self.frameFood, text=">>", width=10, height=2, bg="gray", fg="black", command=lambda: self.jumpRecFood(5))
        self.btnFwdFood = tk.Button(self.frameFood, text=">", width=10, height=2, bg="gray", fg="black", command=lambda: self.jumpRecFood(1))
        self.btnEndFood = tk.Button(self.frameFood, text=">|", width=10, height=2, bg="gray", fg="black", command=lambda: self.jumpRecFood(len(self.sql.recordsFood)-1))

        self.lblFeedback = tk.Label(self.frameFood, text="Press Connect to Begin.", width=20, bg="white", fg="black", relief="sunken")
        self.lblFeedback.place(x=700, y=700)

        self.btnStartFood.place(x=100, y=500)
        self.btnPrevFood.place(x=200, y=500)
        self.btnRewindFood.place(x=300, y=500)
        self.btnFastForwardFood.place(x=400, y=500)
        self.btnFwdFood.place(x=500, y=500)
        self.btnEndFood.place(x=600, y=500)

        self.btnNewFood = tk.Button(self.frameFood, text="New Food", width=10, height=2, bg="gray", fg="black", command=lambda: self.insertFood())
        self.btnUpdateFood = tk.Button(self.frameFood, text="Update Food", width=10, height=2, bg="gray", fg="black", command=self.saveChangedFood())
        self.btnDeleteFood = tk.Button(self.frameFood, text="Delete Food", width=10, height=2, bg="gray", fg="black", command=self.showConfirmAlertFood())

        self.btnNewFood.place(x=100, y=600)
        self.btnUpdateFood.place(x=200, y=600)
        self.btnDeleteFood.place(x=300, y=600)

        self.notebook.add(self.frameFood, text="Food")
        
        self.foodId = 0

        self.mainWin.mainloop()



    def showDialogAlert(self):
        tk.messagebox.showwarning(title="Button Clicked", message="This button click has not been handeled yet.")

    def showAboutAlert(self):
        tk.showwarning(title="About Fitness", message="Fitness Tracking Database Program. Master Project.")

    def showConfirmAlertFood(self):
        pass

    def showConfirmAlertFood(self):
        pass

    def connectionManager(self):
        self.sql.connect()

    #Create part of CRUD (Crud)

    def setFoodBlanks(self):
        pass
    def setDayBlanks(self):
        pass
    def insertFood(self):
        pass

    def insertDay(self):
        pass
    def connect(self):
        pass
    
    #Read part of CRUD (cRud)

    def retreiveFood(self):
        pass
    def retreiveDay(self):
        pass
    def showRecordFood(self, recordFood):
        pass
    def showRecordDay(self, recordDay):
        pass
    def saveChangedFood(self):
        pass
    def deleteRecordFood(self, foodId):
        pass

    def deleteRecordDay(self, dayID):
        pass
    def setToZero(self):
        pass
    def jumpRecFood(self, jumpFood):
        pass

    def jumpRecDay(self, jumpDay):
        pass
    

        

    



