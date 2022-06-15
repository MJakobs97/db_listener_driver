from time import sleep
from multiprocessing import Process
import threading
from gpiozero import LED, Buzzer, TonalBuzzer

led=""
tb=""


def construct_msg(doc, nrClients):
 msg = "ID|BAT|DSK|GPS|REC\n"

 for i in range(nrClients):
  print("Client Nr: %i \n", i)
  id =str(doc['data'][i]['address'])+"|"
  id_tmp = id.split(":")
  id = id_tmp[-2]+":"+id_tmp[-1]
  bat=str(doc['data'][i]['battery'])+"%|"
  dsk=str(int(int(doc['data'][i]['disk'])/1024/1024))+"G|"
  tgps = int(doc['data'][i]['gps'])
  gps=("Y" if tgps else "N")+"|"       
  #aenc = int(doc['data'][i]['aenc'])
  #rec=("Y" if aenc else "N")+"|"   
  rec="_"
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
  #rec=doc['data'][i]['aenc']

  # Hacky fixes
  # 
  
  bat=str(50)
  gps="1"

  if (int(bat)<bat_thrshld or int(dsk)<dsk_thrshld or gps !="1"):
    error = True
    errorID.append(i)
    errorMSG += "C%d " %(i)
    if int(bat)<bat_thrshld:
     errorMSG +="BAT "
    if int(dsk)<dsk_thrshld:
     errorMSG +="DISK "
    if gps !="1":
     errorMSG += "GPS "
    #if rec !="1":
     #errorMSG += "REC"
    errorMSG += "\n"
    clientID = id
 return error, errorID, errorMSG, clientID

def init_gpio():
 try:
   global led
   led = LED(26)
   global tb
   tb = TonalBuzzer(16)

   notes = ["A4", "C5", "D5", "E5", "F5", "E5", "D5", "B4", "G4"]
   times = [0.25, 0.5, 0.25, 0.375, 0.125, 0.25, 0.5, 0.25, 0.375]

   for i in range(len(notes)):
    tb.play(notes[i])
    sleep(times[i])
   tb.stop()   

 except Exception as ex:
  print("Exception in init_gpio(): \n", str(ex))


def error_blink():
  #exchange print statements with GPIO hi/low for LED
  try: 
   global led 
   led.off()  
   led.blink(on_time=0.05, off_time=0.15)
   sleep(7.5)
   led.off()
  
  except Exception as ex:
   #print("Exception: Blink!\n", str(ex))
   print("blink")

def error_beep():
  #exchange print statements with GPIO hi/low for BUZZER
  try:
   global tb
   tb.stop()
   for i in range(3):
    tb.play("A5")
    sleep(0.125)
    tb.stop()
    sleep(0.125)
   tb.stop()
  
  except Exception as ex:   
   #print("Exception: Beep!\n", str(ex))
   print("möp!")
  
   
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

def threadwarn():
 thread_blink = threading.Thread(target=error_blink)
 thread_blink.daemon=True
 thread_blink.start()

 thread_beep = threading.Thread(target=error_beep)
 thread_beep.daemon=True
 thread_beep.start()