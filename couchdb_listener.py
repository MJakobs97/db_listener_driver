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

sleep(10)
try:
 for changes in db.changes(feed="continuous", heartbeat=50000):
  print(changes)
  #doc = db[changes[id]]
  #print("Data is: "+ str(doc['data'][0])+"\n")
  msg = ""

  #sleep(5)

except Exception as ex:
 print("Error: \n", str(ex))






