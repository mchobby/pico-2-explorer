from machine import Pin,ADC
from rtplay import *
import sys

# Désactive PowerSafe (lower ripple)
Pin( 23, Pin.OUT, value=True )

# Pin used by the Buzzer
buzzer = RingTonePlayer( Pin.board.GP13 )
buzzer.play_str( 'Monty Python:d=8,o=5,b=180:d#6,d6' )

p1_in = Pin( 18, Pin.IN, Pin.PULL_UP )
p2_in = Pin( 17, Pin.IN, Pin.PULL_UP )
p3_in = Pin( 16, Pin.IN, Pin.PULL_UP )
l1 = Pin( 22, Pin.OUT, False )
l2 = Pin( 21, Pin.OUT, False )
l3 = Pin( 20, Pin.OUT, False )
a0 = ADC( Pin( Pin.board.GP26 ) )
a1 = ADC( Pin( Pin.board.GP27 ) )
a2 = ADC( Pin( Pin.board.GP28 ) )


def calc_temp( millivolts ):
    return (millivolts-500)/10


while True:
	if (p2_in.value()==0) and (p3_in.value()==0):
		sys.exit()


	if p1_in.value()==0:
		buzzer.play_str( 'Monty Python:d=8,o=5,b=180:d#6,d6' )
		l1.toggle()

	if p2_in.value()==0:
		buzzer.play_str( 'Monty Python:d=8,o=5,b=180:4c6,b' )
		l2.toggle()

	if p3_in.value()==0:
		buzzer.play_str( 'Monty Python:d=8,o=5,b=180:4a#,a' )
		l3.toggle()

	# Analog reads
	val0 = 0
	val1 = 0
	val2 = 0
	for i in range( 10 ):
		val0 += a0.read_u16()
		val1 += a1.read_u16()
		val2 += a2.read_u16()
	val0 = val0/10	 # calculer la moyenne
	val1 = val1/10	 # calculer la moyenne
	val2 = val2/10	 # calculer la moyenne

	# temperature
	mv = 3300*val0/65535
	temp = calc_temp( mv )
	print( 'Pot(a2)=%5i | temp=%2.2f C | Ldr=%5i' % (val2, temp, val1) )


	time.sleep_ms(100)
