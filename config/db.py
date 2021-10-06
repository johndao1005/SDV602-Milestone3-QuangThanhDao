
from pymongo import MongoClient
from dotenv import load_dotenv
from pathlib import Path
import os
import certifi
ca = certifi.where()
load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

MONGO_URI = os.getenv("MONGO_URI")
def connectDB():
    try:
        client = MongoClient(f"{MONGO_URI}",tlsCAFile=ca)
        print("Connect to Database")
        return client["white-shark"]
    except:
        print("Connection failed")

if __name__ == "__main__":
    connectDB()