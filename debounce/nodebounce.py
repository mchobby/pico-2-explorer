from machine import Pin

counter = 0
last_counter = 0

p_in = Pin( 10, Pin.IN, Pin.PULL_UP )
last_state = p_in.value()
while True:
    # lecture de l'état
    state = p_in.value()
    if state!=last_state:
        # raising edge
        if state == 0:
            counter += 1
        last_state = state
        continue
    
    if counter != last_counter:
        print( counter )
        last_counter = counter

