import couchdb
import sys
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106
from time import sleep

serial = i2c(port=1, address=0x3c)

device = sh1106(serial)

couch = couchdb.Server()
database_name = "gopro_stats"

while database_name not in couch:
 with canvas(device) as draw:
  msg = "DB document not initialized!\n Please wait ..."
  draw.text((15,32),msg, fill="white")

db=""

try:
 db = couch[database_name]
except Exception as ex:
 with canvas(device) as draw:
  msg = "DB connection Error!"
  draw.text((0,32),msg, fill="white")
  sleep(5)
  sys.exit("DB connection error, restarting listener...")

with canvas(device) as draw:
 msg = "DB connection successful!"
 draw.text((0,32),msg, fill="white")

id = ""

while id not in db:
 with canvas(device) as draw:
  draw.text((0,32),"Currently no suitable\ndata in db", fill="white")
 sleep(5)
 for id in db:
  print(id)

for doc_id in db:
 id = doc_id

"""
Wertebereiche:
BAT 10%
DSK 5GB
GPS Y/N
REC Y/N
"""

for changes in db.changes(feed="continuous",heartbeat=1000):
 try:
  #print(changes["id"])
  
  #data acquisition:
  if changes["id"] in db:
   doc = db[changes["id"]]
   nrClients = len(doc['data'])

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



   with canvas(device) as draw:
    draw.text((0,0),msg,fill="white")

 except Exception as ex:
  print("Error: \n", str(ex))

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
  if (bat<15 | dsk<10 | gps == 0):
    error = True
    errorID.append(i)
 return error, errorID


