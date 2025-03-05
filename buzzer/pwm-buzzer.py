from machine import Pin, ADC, PWM
from maps import map
import time

# Désactive PowerSafe (lower ripple)
Pin( 23, Pin.OUT, value=True )

a0 = ADC( Pin( Pin.board.GP26 ) )
buzzer = PWM( Pin( Pin.board.GP13 ) )
buzzer.duty_u16( 65535//3 )
while True:
    val = a0.read_u16()
    hertz = int( map(val, 0, 65535, 100, 10000 ) )
    buzzer.freq( hertz )
    print( 'frequence = %5i Hz' % (hertz) )
    time.sleep_ms( 100 )

