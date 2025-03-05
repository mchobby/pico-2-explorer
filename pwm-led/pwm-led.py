from machine import Pin, ADC, PWM
import time

# Désactive PowerSafe (lower ripple)
Pin( 23, Pin.OUT, value=True )

a0 = ADC( Pin( Pin.board.GP26 ) )
led = PWM( Pin( Pin.board.GP2 ) )
led.freq( 500 )
while True:
    val = a0.read_u16()
    led.duty_u16( val )
    print( 'adc=duty_u16= %5i' % (val) )
    time.sleep_ms( 100 )

