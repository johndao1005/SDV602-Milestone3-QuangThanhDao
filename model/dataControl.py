"""
Model class which contain method to get the raw data from csv DataManager, merge files or read the location data with pandas.
After that filter the data in different catogeries with different methods such as featureData, locationData and genderData
"""
from model.connect import DataHandler
import pandas as pd
import csv


class Model():
    """Model class to process the data as well as read any csv file for upload
    """

    def __init__(self):
        """create an instance of data handler from connection as well as a copy of data collection and store in self.data
        """
        self.dataHandler = DataHandler()
        self.data = self.dataHandler.retrieveData()

    def readFile(self, filePath):
        """function handle reading the data from csv file

        Args:
            filePath (string): the path to retrieve the file

        Returns:
            list: data from csv store in list 
        """
        with open(filePath, 'r', newline="") as data:
            dataset = csv.DictReader(data)
            output = []
            for row in dataset:
                output.append(row)
            return output

    def upload(self, filePath):
        """function handle upload data from csv file to the database

        Args:
            filePath (string): path to file
        """
        newData = self.readFile(filePath)
        self.dataHandler.uploadData(newData)

    def genderData(self):
        """function to filter data for gender DES

        Returns:
            dictionary: data for gender DES
        """
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
        """function return data for feature DES

        Returns:
            dict: data for feature DES
        """
        data = self.data
        yearData = dict()
        for row in data:
            year = row['year']
            if year not in yearData and year != "":
                yearData[year] = [0]*7
            if year != "" and row['occurrenceRemarks'] != "":
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
        """function return data for location DES using pandas

        Returns:
            list: pandas formatted data for location
        """
        locationData = pd.DataFrame.from_records(self.dataHandler.database.find(
            {'master': {'$exists': False}}, {'decimalLatitude': 1, 'decimalLongitude': 1, '_id': 0}))
        locationData['decimalLatitude'] = locationData['decimalLatitude'].astype(
            float)
        locationData['decimalLongitude'] = locationData['decimalLongitude'].astype(
            float)
        return locationData
