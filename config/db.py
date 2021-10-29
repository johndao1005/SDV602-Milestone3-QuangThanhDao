
from pymongo import MongoClient
from dotenv import load_dotenv
from pathlib import Path
import os
import certifi
ca = certifi.where()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

MONGO_URI = os.getenv("MONGO_URI")
def connectDB():
    try:
        client = MongoClient(f"{MONGO_URI}",tlsCAFile=ca)
        return client["white-shark"]
    except:
        print("Connection failed")
        