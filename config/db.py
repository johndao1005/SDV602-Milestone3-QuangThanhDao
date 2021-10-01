
from pymongo import MongoClient
from pprint import pprint
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

MONGO_URI = os.getenv("MONGO_URI")
def connectDB():
    try:
        client = MongoClient(f"{MONGO_URI}")
        print(f"Connected to Database")
        return client["white-shark"]
    except:
        print("Connection failed")
    
if __name__ == "__main__":
    connectDB()