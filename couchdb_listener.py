import couchdb
import sys
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106
from time import sleep

serial = i2c(port=1, address=0x3c)

device = sh1106(serial)
#iter = 0
#while iter < 3:
# with canvas(device) as draw:
#  draw.rectangle(device.bounding_box, outline="white",fill="black")
#  msg = "Hello World " + str(iter)
#  draw.text((30,40),msg, fill="white")
#  iter +=1
#  sleep(10)

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

#sleep(5)

id = ""

while id not in db:
 with canvas(device) as draw:
  draw.text((0,32),"Currently no suitable\ndata in db", fill="white")
 sleep(5)
 for id in db:
  print(id)

#sleep(10)

for doc_id in db:
 id = doc_id



for changes in db.changes(feed="continuous",heartbeat=1000):
 try:
  #print(changes["id"])
  if changes["id"] in db:
   doc = db[changes["id"]]
   print("Data is: "+ str(doc['data'][0])+"\n")
   msg = "BAT |DSK |GPS |Rec \n"
   
   bat=str(doc['data'][0]['battery'])+"%| "
   
   dsk=str(int(int(doc['data'][0]['disk'])/1024/1024))+"GB| "
   
   tmp = doc['data'][0]['gps']
   #tgps = True if tmp == 1 else False
   tgps = ""
   if tmp == 0:
    tgps = False
   elif tmp == 1:
    tgps = True
   gps=("y" if tgps else "n")+"| "
   
   tmp = doc['data'][0]['aenc']
   aenc=("y" if tmp else "n")+"| "
   
   msg+=bat+dsk+gps+aenc
   with canvas(device) as draw:
    draw.text((0,10),msg,fill="white")

  #sleep(5)

 except Exception as ex:
  print("Error: \n", str(ex))






