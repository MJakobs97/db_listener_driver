def construct_msg(doc, nrClients):
 #print("Data is: "+ str(doc['data'][0])+"\n")
 msg = "ID|BAT|DSK|GPS|REC\n"

 for i in range(nrClients):
  print(i)
  id =str(doc['data'][i]['address'])+"|"
  bat=str(doc['data'][i]['battery'])+"%|"
  dsk=str(int(int(doc['data'][i]['disk'])/1024/1024))+"GB|"
  tmp = doc['data'][i]['gps']
  #tgps = True if tmp == 1 else False
  tgps = ""
  if tmp == 0:
   tgps = False
  elif tmp == 1:
   tgps = True
  gps=("y" if tgps else "n")+"|"       
  tmp = doc['data'][i]['aenc']
  rec=("y" if tmp else "n")+"|"   
  msg+=id+bat+dsk+gps+rec+"\n"

 return msg

def analyze(doc, nrClients):
 error=False
 errorID=[]
 
 for i in range(nrClients):
  id =str(doc['data'][i]['address'])
  bat=str(doc['data'][i]['battery'])
  dsk=str(int(int(doc['data'][i]['disk'])/1024/1024))
  gps=doc['data'][i]['gps']
  rec=doc['data'][i]['aenc']

  #currently ignore rec
  if (int(bat)<15 or int(dsk)<10 or gps =="0"):
    error = True
    errorID.append(i)
 return error, errorID

