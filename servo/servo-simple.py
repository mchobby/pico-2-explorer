from machine import Pin
from servo import Servo
import time

s = Servo( Pin.board.GP22 )
for i in range( 5 ):
    s.angle(0)
    time.sleep(2)
    s.angle(45)
    time.sleep(2)
    s.angle(90)
    time.sleep(2)
s.detach()
print( "That s all folks!")
