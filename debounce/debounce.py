from machine import Pin
import time

counter = 0
last_counter = 0

p_in = Pin( 10, Pin.IN, Pin.PULL_UP )
last_state = p_in.value()

while True:
    state = p_in.value()
    if state!=last_state:
        time.sleep_ms(10)
        state2 = p_in.value()
        if state != state2:
            continue
        if state == 0:
            counter += 1
        last_state = state
        continue

    if counter != last_counter:
        print( counter )
        last_counter = counter
