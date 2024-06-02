from src.utils.mongodb import MongoConnection
from src.utils.common import random_text

from dotenv import load_dotenv
from datetime import datetime

import os
import pandas as pd

load_dotenv()


class DashBoardOperations:
    def __init__(self):
        self.mongo_client = MongoConnection().get_client()
        self.db = self.mongo_client[os.getenv("DB")]
        self.collection = self.db[os.getenv("DASHBOARD_COLLECTION")]
    
    def find_conversations(self, user_id: str):
        if self.collection.find_one({"user_id": user_id}) is None:
            return []
        docs = [{"conversation_id": doc["conversation_id"], "conversation_name": doc["conversation_name"], "date_recent": doc["date_recent"]} for doc in self.collection.find({"user_id": user_id}, {"_id": 0})]
        df = pd.DataFrame(docs)
        df["date_recent"] = pd.to_datetime(df["date_recent"])
        df = df.sort_values("date_recent")
        return df.to_dict(orient="records")
    
    def add_conversation(self, user_id: str, conversation_name: str, source: str, source_language: str):
        id = random_text(int(os.getenv("CONVERSATION_ID_LEN")))
        self.collection.insert_one({"user_id": user_id, "conversation_id": id, "conversation_name": conversation_name, "source": source, "source_language": source_language, "date_added": datetime.now(), "date_recent": datetime.now()})
        return id
    
    def update_recent_date(self, user_id: str, conversation_id: str):
        self.collection.update_one({"user_id": user_id, "conversation_id": conversation_id}, {"$set": {"date_recent": datetime.now()}})
        return True

    def delete_conversation(self, user_id: str, conversation_id: str):
        self.collection.delete_one({"user_id": user_id, "conversation_id": conversation_id})
        return True
