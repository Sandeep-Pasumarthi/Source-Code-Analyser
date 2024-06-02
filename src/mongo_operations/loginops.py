from src.utils.mongodb import MongoConnection
from dotenv import load_dotenv
from src.utils.common import random_text

import os

load_dotenv()


class LoginOperations:
    def __init__(self):
        self.mongo_client = MongoConnection().get_client()
        self.db = self.mongo_client[os.getenv("DB")]
        self.collection = self.db[os.getenv("LOGIN_COLLECTION")]
    
    def is_user_present(self, user_mail: str) -> bool:
        if self.collection.find_one({"mail": user_mail}):
            return True
        return False
    
    def add_user(self, user_mail: str, user_name: str, user_password: str) -> str | bool:
        if not self.is_user_present(user_mail):
            id = random_text(int(os.getenv("USER_ID_LEN")))
            self.collection.insert_one({"id": id, "mail": user_mail, "name": user_name, "password":  user_password})
            return id
        else:
            return False
    
    def validate_user(self, user_mail: str, user_password: str) -> str | bool:
        if self.is_user_present(user_mail):
            user = self.collection.find_one({"mail": user_mail, "password":  user_password}, {"_id": 0, "id": 1})
            if user:
                return user["id"]
            else:
                return False
        else:
            return False
