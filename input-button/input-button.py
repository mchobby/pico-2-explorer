from machine import Pin
import time

p_in = Pin( 10, Pin.IN, Pin.PULL_UP )
while True:
    # lecture de l'état
    v = p_in.value()
    print( v )
    if v==0:
        print( 'PRESS' )
    else:
        print( '---' )

    time.sleep(1)

