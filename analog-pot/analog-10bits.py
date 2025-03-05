from machine import Pin, ADC
import time

# Désactive PowerSafe (lower ripple)
Pin( 23, Pin.OUT, value=True )

a0 = ADC( Pin( Pin.board.GP26 ) )
while True:
    # Effectuer 10 mesures
    val = 0
    for i in range( 10 ):
        val += (a0.read_u16()>>6)
    # calculer la moyenne
    val = val/10
    
    # Calculer la tension
    volt = val*3.3/1023
    print( 'adc_10bits=%5i , volt=%1.2f' % (val,volt) )
    time.sleep_ms( 300 )

