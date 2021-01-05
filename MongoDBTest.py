import pymongo
myclient = pymongo.MongoClient("mongodb://________________:27017/")
mydb = myclient["IoT"]
print(myclient.list_database_names())
print(mydb.list_collection_names())