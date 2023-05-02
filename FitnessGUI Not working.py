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

        if (not self.sql.connected):
            self.connectButton = tk.Button(self.frameFood, text="Connect", width=10, height=2, bg="gray", fg="black", command=self.connectionManager)
        else:
            self.connectButton = tk.Button(self.frameFood, text="Disconnect", width=10, height=2, bg="gray", fg="black", command=self.connectionManager)
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
        message = "Press OK to delete Food record for: \n" + self.foodNameEntry.get()
        if (tk.messagebox.askyesnocancel(title="Confirm Delete", message = message)):
            self.answer = self.deleteRecordFood(self.foodId)
            self.lblFeedback.config(text=self.answer)
        else:
            self.lblFeedback.config(text=self.answer)

    def showConfirmAlertFood(self):
        message = "Press OK to delete Food record for: \n" + self.foodNameEntry.get()
        if (tk.messagebox.askyesnocancel(title="Confirm Delete", message = message)):
            self.answer = self.deleteRecordFood(self.foodId)
            self.lblFeedback.config(text=self.answer)
        else:
            self.lblFeedback.config(text=self.answer)


    def connectionManager(self):
        if(not self.sql.connected):
            self.answer = self.sql.connect()
            self.connectionButton.config(activebackground="green", fg="black", text="Disconnect")
            self.sql.connected = True
            self.sql.getDay()
            self.sql.getFood
            self.showRecordFood(0)
            self.showRecordDay(0)
            self.lblFeedback.config(text=self.answer)
        else:
            self.answer = self.sql.disconnect()
            self.connectionButton.config(activebackground="red", fg="black", text="Connect")
            self.sql.connected = False
            self.currentRecordFood = 0
            self.currentRecordDay = 0
            self.lblFeedback.config(text=self.answer)

    #Create part of CRUD (Crud)

    def setFoodBlanks(self):
        self.foodDayEntry.delete(0, tk.END)
        self.foodNameEntry.delete(0, tk.END)
        self.foodCalEntry.delete(0, tk.END)
        self.foodProteinEntry.delete(0, tk.END)
        self.foodFiberEntry.delete(0, tk.END)
        self.foodCarbEntry.delete(0, tk.END)
        self.foodFatEntry.delete(0, tk.END)

    def setDayBlanks(self):
        self.dayDateEntry.delete(0, tk.END)
        self.dayStepsEntry.delete(0, tk.END)
        self.dayCalConsumedEntry.delete(0, tk.END)
        self.dayCalBurntEntry.delete(0, tk.END)
        self.dayRestingHREntry.delete(0, tk.END)
        self.dayActiveHREntry.delete(0, tk.END)
    
    def insertFood(self):
        if (not self.midInsert):
            self.setFoodBlanks()
            self.btnNew.config(text="Commit Insetion")
            self.midInsert = True
        else:
            self.retrieveFood()
            self.answer = self.sql.newFood()
            self.btnNew.config(text="New Food")
            self.midInsert = False
            self.lblFeedback.config(text=self.answer)

    def insertDay(self):
        if (not self.midInsert):
            self.setDayBlanks()
            self.btnNew.config(text="Commit Insetion")
            self.midInsert = True
        else:
            self.retrieveDay()
            self.answer = self.sql.newDay()
            self.btnNew.config(text="New Food")
            self.midInsert = False
            self.lblFeedback.config(text=self.answer)
    
    #Read part of CRUD (cRud)

    def retreiveFood(self):
        self.FoodDayKey = self.foodDayEntry.get()
        self.FoodName = self.foodNameEntry.get()
        self.FoodCal = self.foodCalEntry.get()
        self.FoodProtein = self.foodProteinEntry.get()
        self.FoodFiber = self.foodFiberEntry.get()
        self.FoodCarb = self.foodCarbEntry.get()
        self.foodFat = self.foodFatEntry.get()
        self.sql.insertRecordFood = [self.FoodDayKey, self.FoodName, self.FoodCal, self.FoodProtein, self.FoodFiber, self.FoodCarb, self.foodFat]

    def retreiveDay(self):
        self.dayDate = self.dayDateEntry.get()
        self.daySteps = self.dayStepsEntry.get()
        self.dayCalConsumed = self.dayCalConsumedEntry.get()
        self.dayCalBurned = self.dayCalBurnedEntry.get()
        self.dayRestingHR = self.dayRestingHREntry.get()
        self.dayActiveHR = self.dayActiveHREntry.get()
        self.sql.insertRecordDay = [self.dayDate, self.daySteps, self.dayCalConsumed, self.dayCalBurned, self.dayRestingHR, self.dayActiveHR]

    def showRecordFood(self, recordFood):
        self.holdRecordFood = self.sql.recordsFood[recordFood]
        (self.foodId, self.FoodDayKey, self.FoodName, self.FoodCal, self.FoodProtein, self.FoodFiber, self.FoodCarb, self.foodFat) = self.holdRecordFood

        self.foodDayEntry.delete(0, tk.END)
        self.foodNameEntry.delete(0, tk.END)
        self.foodCalEntry.delete(0, tk.END)
        self.foodProteinEntry.delete(0, tk.END)
        self.foodFiberEntry.delete(0, tk.END)
        self.foodCarbEntry.delete(0, tk.END)
        self.foodFatEntry.delete(0, tk.END)

        self.foodDayEntry.insert(0, self.FoodDayKey)
        self.foodNameEntry.insert(0, self.FoodName)
        self.foodCalEntry.insert(0, self.FoodCal)
        self.foodProteinEntry.insert(0, self.FoodProtein)
        self.foodFiberEntry.insert(0, self.FoodFiber)
        self.foodCarbEntry.insert(0, self.FoodCarb)
        self.foodFatEntry.insert(0, self.foodFat)

        self.lblFeedback.config(text="Record ID: " + str(self.foodId))

    def showRecordDay(self, recordDay):

        self.holdRecordDay = self.sql.recordsDay[recordDay]
        (self.dayId, self.dayDate, self.daySteps, self.dayCalConsumed, self.dayCalBurned, self.dayRestingHR, self.dayActiveHR) = self.holdRecordDay

        self.dayDateEntry.delete(0, tk.END)
        self.dayStepsEntry.delete(0, tk.END)
        self.dayCalConsumedEntry.delete(0, tk.END)
        self.dayCalBurnedEntry.delete(0, tk.END)
        self.dayRestingHREntry.delete(0, tk.END)
        self.dayActiveHREntry.delete(0, tk.END)

        self.dayDateEntry.insert(0, self.dayDate)
        self.dayStepsEntry.insert(0, self.daySteps)
        self.dayCalConsumedEntry.insert(0, self.dayCalConsumed)
        self.dayCalBurnedEntry.insert(0, self.dayCalBurned)
        self.dayRestingHREntry.insert(0, self.dayRestingHR)
        self.dayActiveHREntry.insert(0, self.dayActiveHR)

        self.lblFeedback.config(text="Record ID: " + str(self.dayId))

    def saveChangedFood(self):
        #foodId = self.foodId
        self.FoodDayKey = self.foodDayEntry.get()
        self.FoodName = self.foodNameEntry.get()
        self.FoodCal = self.foodCalEntry.get()
        self.FoodProtein = self.foodProteinEntry.get()
        self.FoodFiber = self.foodFiberEntry.get()
        self.FoodCarb = self.foodCarbEntry.get()
        self.foodFat = self.foodFatEntry.get()

        self.sql.updateRecordFood = [0, self.FoodDayKey, self.FoodName, self.FoodCal, self.FoodProtein, self.FoodFiber, self.FoodCarb, self.foodFat, self.foodId]
        self.answer = self.sql.updateFood()

        self.answer = self.sql.loadFood()
        self.showRecordFood(0)
        self.lblFeedback.config(text=self.answer)

    def deleteRecordFood(self, foodId):
        self.answer = self.result = self.sql.deleteFood(foodId)
        self.lblFeedback.config(text=self.answer)

        self.currentRecordFood = self.currentRecordFood - 1
        self.lblFeedback.config(text=self.answer)

    def deleteRecordDay(self, dayID):
        self.answer = self.result = self.sql.deleteDay(dayID)
        self.lblFeedback.config(text=self.answer)

        self.currentRecordDay = self.currentRecordDay - 1
        self.lblFeedback.config(text=self.answer)

    def setToZero(self):
        self.currentRecordDay = 0
        self.currentRecordFood = 0

    def jumpRecFood(self, jumpFood):
        self.currentRecordFood += jumpFood
        if (self.currentRecordFood >- len(self.sql.recordsFood)):
            self.currentRecordFood = len(self.sql.recordsFood) - 1
        if(self.currentRecordFood < 0):
            self.currentRecordFood = 0
        self.showRecordFood(self.currentRecordFood)

    def jumpRecDay(self, jumpDay):
        self.currentRecordDay += jumpDay
        if (self.currentRecordDay >- len(self.sql.recordsDay)):
            self.currentRecordDay = len(self.sql.recordsDay) - 1
        if(self.currentRecordDay < 0):
            self.currentRecordDay = 0
        self.showRecordDay(self.currentRecordDay)
    
    

        

    




