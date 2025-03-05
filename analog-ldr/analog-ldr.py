from machine import Pin, ADC
import time

TURN_ON = 32000 # 0 - 65535

# Désactive PowerSafe (lower ripple)
Pin( 23, Pin.OUT, value=True )

a1 = ADC( Pin( Pin.board.GP27 ) )
led = Pin( Pin.board.GP22, Pin.OUT )
while True:
    # Effectuer 10 mesures
    val = 0
    for i in range( 10 ):
        val += a1.read_u16()
    # calculer la moyenne
    val = val/10
    
    led_value = val < TURN_ON
    led.value( led_value )
    print( 'adc=%5i , led=%5i' % (val,10000 if led_value==True else 0) )
    time.sleep_ms( 300 )

