import pymongo
from dotenv import load_dotenv
from pathlib import Path
import os
import certifi

ca = certifi.where()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

MONGO_URI = os.getenv("MONGO_URI")

def connectDB():
    print('start')
    print(f'{MONGO_URI}')
    try:
        client = pymongo.MongoClient(f"{MONGO_URI}",tlsCAFile=ca)
        print("Connect to Database")
        return client["white-shark"]
    except pymongo.errors.ConnectionFailure as e:
        print(e)