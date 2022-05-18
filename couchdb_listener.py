import couchdb
import sys
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106
from time import sleep
from docDataFunc import analyze, construct_msg, multiwarn, error_beep, error_blink

serial = i2c(port=3, address=0x3c)

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
   error, errorID, errorMSG = analyze(doc, nrClients)

   device.clear()
   with canvas(device) as draw:
    if not error:
     msg = construct_msg(doc, nrClients)
     draw.text((0,0),msg,fill="white")
    elif error:
     msg = "Error:\n"+errorMSG
     #draw.rectangle(device.bounding_box, outline="white", fill="white")
     draw.text((0,0),msg,fill="white")
     multiwarn()
     

 except Exception as ex:
  print("Error: \n", str(ex))
  print("Failing in main changes listening loop")






