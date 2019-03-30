import pymongo
from userbot import MONGODB

myclient = pymongo.MongoClient(MONGODB)

mydb = myclient["userbot"]
