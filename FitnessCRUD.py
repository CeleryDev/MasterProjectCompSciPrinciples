"""
FOOD CRUD
Benjamin Feibus
5th Period
CS50 AP
Cmdr Schenk
Thur Apr 13 2023
"""

import mysql.connector

class mySQLFunctions:
    def __init__(self):
        self.connected = False
        self.recordsFood = []
        self.recordsDay = []
        self.cached = ()
        self.index = 0
        self.insertRecordFood = [0, "", 0, 0, 0, 0, 0]
        self.updateRecordFood = [0, 0, "", 0, 0, 0, 0, 0]
        self.insertRecordDay = ["", 0, 0, 0, 0, 0]
        self.updateRecordDay = [0, "", 0, 0, 0, 0, 0]

    def connect(self):
        if not self.connected:
            try:
                self.sqlConnection = mysql.connector.connect(user='root',
                                                             password='12345678',
                                                             host='localhost',
                                                             database='FitnessScheme')
                self.c = self.sqlConnection.cursor()
                self.connected = True
                return "Connected"
            except mysql.connector.Error as error:
                return "Failed to connect: ", error
        
    def disconnect(self):
        if self.connected:
            self.sqlConnection.close()
            self.connected = False
            self.cached = ()
            self.index = 0
            return "Connection Closed"

    def newFood(self):
        self.c.execute(
            """
            INSERT INTO Food (food_name, day_key, caloric_value,
              protein_value, fiber_value, carb_value, total_fat_value)
                VALUES (%s, %s, %s, %s, %s, %s %s);
            """, self.insertRecordFood)
        self.sqlConnection.commit()

    def editFood(self):
        self.c.execute("UPDATE Food SET food_name = "+ str(self.updateRecordFood[2]) + ", day_key = "+ str(self.updateRecordFood[1]) + ", caloric_value = "+ str(self.updateRecordFood[3]) + ", protein_value = "+ str(self.updateRecordFood[4]) + ", fiber_value = "+ str(self.updateRecordFood[5]) + ", carb_value = "+ str(self.updateRecordFood[6]) + ", total_fat_value = "+ str(self.updateRecordFood[7]) + "WHERE id = " + str(self.updateRecordFood[0]) + ";")
    
    def deleteFood(self):
        try:
            self.c.execute("DELETE FROM Food WHERE id =" + self.index + ";")
            self.sqlConnection.commit()
            self.getFood()
            return "Record Successfully Deleted"
        except mysql.connector.Error as error:
            return "Failed to delete: ", error
        
    
    def getFood(self):
        try:
            self.c.execute("SELECT * FROM Food;")
            self.recordsFood = self.c.fetchall()
        except mysql.connector.Error as error:
            return "Failed to fetch: ", error
        
    def newDay(self):
        self.c.execute(
            """
            INSERT INTO DayStats (day_and_time, total_steps, calories_consumed, calories_burnt, resting_heartrate, active_heartrate)
                VALUES (%s, %s, %s, %s, %s, %s);
            """, self.insertRecordDay)
        self.sqlConnection.commit()
    
    def editDay(self):
        self.c.execute("UPDATE DayStats SET day_and_time = "+ str(self.updateRecordDay[1]) + ", total_steps = "+ str(self.updateRecordDay[2]) + ", calories_consumed = " + str(self.updateRecordDay[3]) + ", calories_burnt = "+ str(self.updateRecordDay[4]) + ", resting_heartrate = "+ str(self.updateRecordDay[5]) + ", active_heartrate = "+ str(self.updateRecordDay[6]) + "WHERE id = " + str(self.updateRecordDay[0]) + ";")

    def deleteDay(self):
        try:
            self.c.execute("DELETE FROM DayStats WHERE id =" + self.index + ";")
            self.sqlConnection.commit()
            self.getDay()
            return "Record Successfully Deleted"
        except mysql.connector.Error as error:
            return "Failed to delete: ", error
    
    def getDay(self):
        try:
            self.c.execute("SELECT * FROM DayStats;")
            self.recordsDay = self.c.fetchall()
        except mysql.connector.Error as error:
            return "Failed to fetch: ", error
        
        

