from time import sleep
from multiprocessing import Process

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
 errorMSG=""
 bat_thrshld = 15
 dsk_thrshld = 10
 
 for i in range(nrClients):
  id =str(doc['data'][i]['address'])
  bat=str(doc['data'][i]['battery'])
  dsk=str(int(int(doc['data'][i]['disk'])/1024/1024))
  gps=doc['data'][i]['gps']
  rec=doc['data'][i]['aenc']

  #currently ignore rec
  
  if (int(bat)<bat_thrshld or int(dsk)<dsk_thrshld or gps !="1" or rec !="1"):
    error = True
    errorID.append(i)
    errorMSG += "C%d " %(i)
    if int(bat)<bat_thrshld:
     errorMSG +="BAT "
    if int(dsk)<dsk_thrshld:
     errorMSG +="DISK "
    if gps !="1":
     errorMSG += "GPS "
    if rec !="1":
     errorMSG += "REC"
    errorMSG += "\n"
 return error, errorID, errorMSG

def error_blink():
  #exchange print statements with GPIO hi/low for LED
  elapsed = 0
  while elapsed < 4:
   sleep(0.4)
   print("LED ON!")
   sleep(0.2)
   print("LED OFF!")
  #Do Stuff with led
   elapsed +=1

def error_beep():
  #exchange print statements with GPIO hi/low for BUZZER
  elapsed = 0
  while elapsed < 4:
   print("BUZZER ON!")
   sleep(0.4)
   print("BUZZER OFF!")
   sleep(0.2)
   elapsed +=1
   
def multiwarn():
 processes = []
 p1 = Process(target=error_blink)
 p1.start()
 processes.append(p1)
 
 p2 = Process(target=error_beep)
 p2.start()
 processes.append(p2)

 for p in processes:
   p.join()

