"""
Read csv file in data-sample folder by defaul but also allow reading data from different file source provided with open-csv function or merge function
"""
import csv
from os import path
import pandas as pd
from typing import Dict


class DataManager():
    def __init__(self):
        self.status: Dict = {}
        self.file: Dict = {}
        self.file = None

    def readFile(self, filePath):
        
        with open(filePath, 'r', newline="") as data:
            dataset = csv.DictReader(data)
            output = []
            for row in dataset:
                output.append(row)
            return output

    def append(self, newFile, currentFile,):
        header = ["ï»¿X", "Y", "FID", "id", "modified", "language", "rights", "rightsHolder", "bibliographicCitation", "institutionCode", "collectionCode", "basisOfRecord", "catalogNumber", "occurrenceRemarks", "individualID", "individualCount", "sex", "occurrenceStatus", "eventDate", "year", "waterBody",
                "decimalLatitude", "decimalLongitude", "geodeticDatum", "coordinateUncertaintyInMeters", "footprintWKT", "georeferenceRemarks", "scientificNameID", "scientificName", "kingdom", "phylum", "class", "order_", "family", "genus", "subgenus", "specificEpithet", "infraspecificEpithet", "scientificNameAuthorship"]
        with open(currentFile, 'a', newline="") as targetData:
            writer = csv.DictWriter(targetData, header,extrasaction='ignore')
            for row in self.readFile(newFile):
                writer.writerow(row)

    def readLocation(self, filePath):
        locationData = pd.read_csv(filePath,
                                usecols=["decimalLatitude",
                                            "decimalLongitude"],
                                )
        return locationData
