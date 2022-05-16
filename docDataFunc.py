def construct_msg(doc, nrClients):
 #print("Data is: "+ str(doc['data'][0])+"\n")
 msg = "ID|BAT|DSK|GPS|REC\n"

 for i in range(nrClients):
  print("Client Nr: %i \n", i)
  id =str(doc['data'][i]['address'])+"|"
  id_tmp = id.split(":")
  id = id_tmp[-2]+":"+id_tmp[-1]
  bat=str(doc['data'][i]['battery'])+"%|"
  dsk=str(int(int(doc['data'][i]['disk'])/1024/1024))+"G|"
  tmp = int(doc['data'][i]['gps'])
  #tgps = True if tmp == 1 else False
  tgps = ""
  if tmp == 0:
   tgps = "N"
  elif tmp == 1:
   tgps = "Y"
  #gps=("y" if tgps else "n")+"|"       
  gps = tgps
  tmp = doc['data'][i]['aenc']
  #rec=("y" if tmp else "n")+"|"   
  rec=tmp
  msg+=id+bat+dsk+gps+rec+"\n"
  print(msg)

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

