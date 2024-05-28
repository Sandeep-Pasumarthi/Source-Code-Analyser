from pymongo import MongoClient
from dotenv import load_dotenv

import os

load_dotenv(os.path.join(os.getcwd(), ".env"))


class MongoConnection:
    def __init__(self):
        self.client = MongoClient(os.getenv("MONGO_URI"))
    
    def get_client(self):
        return self.client
