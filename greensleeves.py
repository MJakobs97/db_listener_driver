from time import sleep
from gpiozero import TonalBuzzer

notes = ["A4", "C5", "D5", "E5", "F5", "E5", "D5", "B4", "G4"]
times = [0.5, 1, 0.5, 0.75, 0.25, 0.5, 1, 0.5, 0.75]

tb = TonalBuzzer(16)

for i in range(len(notes)):
 tb.play(notes[i])
 sleep(times[i])

tb.stop()