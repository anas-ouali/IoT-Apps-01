import pymongo

DevEUI = "_________________"


MongoDBClient = pymongo.MongoClient("mongodb://_________________:27017")
MongoDBDatabase = MongoDBClient["___"]
MongoColumn = MongoDBDatabase["______"]

MongoDBQuery = {"EUI_uplink.DevEUI":DevEUI}
QueryDoc = MongoColumn.find(MongoDBQuery)
print(QueryDoc)
i = 0
for x in QueryDoc:
    print(i, x)
    i = i + 1

MongoDBQuery = {"EUI_downlink.DevEUI":DevEUI}
QueryDoc = MongoColumn.find(MongoDBQuery)
print(QueryDoc)
for x in QueryDoc:
    print(i, x)
    i = i + 1