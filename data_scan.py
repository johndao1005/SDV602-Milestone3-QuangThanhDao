"""
Read csv file in data-sample folder by defaul but also allow reading data from different file source provided with open-csv function or merge function
"""

import pandas as pd
from typing import Dict
from config.db import connectDB

class DataManager():
    def __init__(self):
        self.status: Dict = {}
        self.file: Dict = {}
        self.file = None

    

    
#     def readLocation(self,filePath):
#         db = connectDB()
#         locationData = pd.DataFrame.from_records(db['data'].find({'master':{'$exists':False}},{'decimalLatitude':1,'decimalLongitude':1,'_id':0}))
#         locationData = pd.read_csv(filePath,
#                                 usecols=["decimalLatitude",
#                                             "decimalLongitude"],
#                                 )
#         return locationData

# if __name__ == "__main__":
#     data = DataManager()
#     #print(data.readLocation())
#     print(data.readLocation('./data-sample/test1.csv'))
