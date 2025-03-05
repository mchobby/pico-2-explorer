from machine import Pin, ADC
import time

# Désactive PowerSafe (lower ripple)
Pin( 23, Pin.OUT, value=True )
a1 = ADC( Pin( Pin.board.GP27 ) )
red = Pin( Pin.board.GP20, Pin.OUT )
green = Pin( Pin.board.GP21, Pin.OUT )

def calc_temp( millivolts ):
    return (millivolts-500)/10

while True:
    # Effectuer 10 mesures
    val = 0
    for i in range( 10 ):
        val += a1.read_u16()
    val = val/10     # calculer la moyenne

    mv = 3300*val/65535
    temp = calc_temp( mv )
    print( 'adc=%5i , mv=%5i, temp=%2.2f °C' % (val, mv, temp) )
    
    green.value( 19<=temp<25 )
    red.value( temp>= 25 )
        
    time.sleep_ms( 300 )