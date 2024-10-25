from machine import Pin
import time
p = Pin( 2, Pin.OUT )
p.value( True )
time.sleep(1)
p.value( False ) 
