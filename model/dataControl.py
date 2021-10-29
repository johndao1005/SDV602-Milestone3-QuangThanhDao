"""
Model class which contain method to get the raw data from csv DataManager, merge files or read the location data with pandas.
After that filter the data in different catogeries with different methods such as featureData, locationData and genderData
"""
from model.connect import DataHandler
import pandas as pd
import csv

class Model():
    def __init__(self):
        self.dataHandler = DataHandler()
        self.data = self.dataHandler.retrieveData()

    def readFile(self, filePath):
        with open(filePath, 'r', newline="") as data:
            dataset = csv.DictReader(data)
            output = []
            for row in dataset:
                output.append(row)
            return output
    
    def upload(self, filePath):
        newData = self.readFile(filePath)
        self.dataHandler.uploadData(newData)

    def genderData(self):
        data = self.data
        male = 0
        female = 0
        for row in data:
            if row['sex'] == "male":
                male += 1
            elif row['sex'] == "female":
                female += 1
        return {"Male": male, "Female": female}

    def featureData(self):
        data = self.data
        yearData = dict()
        for row in data:
            year = row['year']
            if year not in yearData and year != "":
                yearData[year] = [0]*7
            if year !="" and row['occurrenceRemarks'] != "":
                featureData = row['occurrenceRemarks'].split(' ')
                if featureData[0] == "Mature":
                    yearData[year][0] += 1
                elif featureData[0] == "Immature":
                    yearData[year][1] += 1
                if featureData[2] == "300":
                    yearData[year][2] += 1
                elif featureData[2] == "350":
                    yearData[year][3] += 1
                elif featureData[2] == "400":
                    yearData[year][4] += 1
                elif featureData[2] == "420-450":
                    yearData[year][5] += 1
                else:
                    yearData[year][6] += 1
        return yearData

    def locationData(self):
        locationData = pd.DataFrame.from_records(self.dataHandler.database.find({'master':{'$exists':False}},{'decimalLatitude':1,'decimalLongitude':1,'_id':0}))
        locationData['decimalLatitude'] = locationData['decimalLatitude'].astype(float)
        locationData['decimalLongitude'] = locationData['decimalLongitude'].astype(float)
        return locationData

