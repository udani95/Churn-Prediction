import pymongo
from bson.objectid import ObjectId
import bcrypt

# MongoDB Connection
client = pymongo.MongoClient("mongodb+srv://udanikaushalya1995:123@cluster0.f8itm.mongodb.net/", tlsAllowInvalidCertificates=True)
db = client.mydatabase
users_collection = db.users

# Function to add a new user (admin)
def add_user(username, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user_data = {
        "username": username,
        "password": hashed_password
    }
    users_collection.insert_one(user_data)

# Function to verify user credentials
def verify_user(username, password):
    user = users_collection.find_one({"username": username})
    if user and bcrypt.checkpw(password.encode('utf-8'), user["password"]):
        return True
    return False

# Function to fetch all users (optional for admin management)
def get_all_users():
    return list(users_collection.find())
