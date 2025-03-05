from machine import Pin, ADC, PWM
from maps import map
import time

# Désactive PowerSafe (lower ripple)
Pin( 23, Pin.OUT, value=True )

# Max value for 9 bits number
max_9bits_val = 0b111111111
a0 = ADC( Pin( Pin.board.GP26 ) )
buzzer = PWM( Pin( Pin.board.GP13 ) )
buzzer.duty_u16( 65535//3 )
while True:
    val = a0.read_u16()
    val_9bits = val >> 7
    hertz = int( map(val_9bits, 0, max_9bits_val , 100, 10000 ) )
    buzzer.freq( hertz )
    print( 'frequence = %5i Hz' % (hertz) )
    time.sleep_ms( 100 )

