from pymongo import MongoClient
import os

MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb+srv://test:test@web-hook-cluster.vk6hhei.mongodb.net/?retryWrites=true&w=majority&appName=web-hook-cluster",
)

client = MongoClient(MONGO_URI)
db = client.github_events
