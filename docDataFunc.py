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
  tgps = int(doc['data'][i]['gps'])
  #gps = Y if tgps == 1 else N
  gps=("Y" if tgps else "N")+"|"       
  aenc = int(doc['data'][i]['aenc'])
  rec=("Y" if aenc else "N")+"|"   
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
  if (int(bat)<15 or int(dsk)<10 or gps !="1"):
    error = True
    errorID.append(i)
 return error, errorID

