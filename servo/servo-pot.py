from machine import Pin, ADC
from servo import Servo
from maps import map
import time

# Désactive PowerSafe (lower ripple)
Pin( 23, Pin.OUT, value=True )

last_ticks = time.ticks_ms()
a0 = ADC( Pin( Pin.board.GP28 ) )
s = Servo( Pin.board.GP22 )
while True:
    # Effectuer 10 mesures
    val = 0
    for i in range( 10 ):
        val += (a0.read_u16()>>6)
    # calculer la moyenne
    val = val/10

    # Conversion Pot -> Angle Servo
    angle = map(val, 0, 1023, 0, 180)
    # Set Servo
    s.angle( int(angle) )
    
    # Affichage toutes les secondes
    if time.ticks_diff( time.ticks_ms(), last_ticks ) > 1000:
        print( 'adc_10bits=%5i , Angle=%3i' % (val, int(angle)) )
        last_ticks = time.ticks_ms()
