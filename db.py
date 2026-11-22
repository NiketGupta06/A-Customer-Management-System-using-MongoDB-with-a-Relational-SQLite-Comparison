from pymongo import MongoClient
from config import MONGO_URI, DB_NAME

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

def test_connection():
    client.admin.command("ping")
    print("Connected to MongoDB Atlas successfully!")

if __name__ == "__main__":
    test_connection()
