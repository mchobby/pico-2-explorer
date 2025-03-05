from machine import Pin, ADC
import time

# Désactive PowerSafe (lower ripple)
Pin( 23, Pin.OUT, value=True )

a0 = ADC( Pin( Pin.board.GP26 ) )
while True:
    val = a0.read_u16()
    volt = val*3.3/65535
    print( 'adc= %5i , volt= %1.2f' % (val,volt) )
    time.sleep_ms( 300 )

