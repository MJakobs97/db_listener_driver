import couchdb
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106
from time import sleep

serial = i2c(port=1, address=0x3c)

device = sh1106(serial)
iter = 0
while iter < 10:
 with canvas(device) as draw:
  draw.rectangle(device.bounding_box, outline="white",fill="black")
  msg = "Hello World " + str(iter)
  draw.text((30,40),msg, fill="white")
  iter +=1
  sleep(10)

couch = couchdb.Server()

db = couch['gopro_stats']

try:
 for changes in db.changes(feed="continuous", heartbeat=50000):
  doc = db[changes["id"]]
  print("Data is: "+ str(doc['data'])+"\n")
  print("Data2 is: "+ str(doc['data2'])+"\n")


  datalist = doc['data2']
  print("Data2 is "+str(len(datalist))+" items long.\n")
  for x in range(len(datalist)):
   print(datalist[x])
   print("\n")
except Exception as ex:
 print("Error: \n", ex)






