import couchdb

couch = couchdb.Server()

db = couch['gopro_stats']

for changes in db.changes(feed="continuous", heartbeat=50000):
 doc = db[changes["id"]]
 #print("Name is: "+doc['name'])
 print("Data is: "+ str(doc['data'])+"\n")
 print("Data2 is: "+ str(doc['data2'])+"\n")


 datalist = doc['data2']
 print("Data2 is "+str(len(datalist))+" items long.\n")
 for x in range(len(datalist)):
  print(datalist[x])
  print("\n")




# print("Datalist is "+str(len(datalist))+" entries long \n")
# print(datalist[0])
# print("Type: "+datalist[0]['type']+"\n")
# print("Data2[1] is: " str(doc['data2'])+"\n")


#doc = {'name':'Employee'}

#db.save(doc)


