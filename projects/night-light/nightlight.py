from machine import Pin, ADC
import time

# Désactive PowerSafe (lower ripple)
Pin( 23, Pin.OUT, value=True )

ldr = ADC( Pin( Pin.board.GP28 ) ) # A2
pot = ADC( Pin( Pin.board.GP27 ) ) # A1
led = Pin( Pin.board.GP20, Pin.OUT )
while True:
	val_ldr = 0
	val_pot = 0
	for i in range(10):
		val_ldr += ldr.read_u16()>>6
		val_pot += pot.read_u16()>>6
	val_ldr //= 10 # 10 bit (0-1023)
	val_pot //= 10

	#print( val_ldr, val_pot)
	led.value( val_ldr < val_pot )
	time.sleep_ms( 20 )