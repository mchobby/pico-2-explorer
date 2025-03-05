from micropython import const
from random import randint
from machine import Pin
from rtplay import *
import time

START_SONG = "Counter Strike - Time Bomb : d=4,o=5,b=100:16c#7,8p,16c#7,8p,16c#7,8p,16c#7"
WIN_SONG = "Black Robb - Whoa : d=4,o=5,b=100:16g,16p,16g6,16a#6,16a6,16a#6,16g6,16p,16g,16p,16g6,16a#6,16a6,16a#6,16g6"
LOOSE_SONG = "dark:d=4,o=5,b=140:8f#6,8e6,2f#6,16e6,16d#6,16d6,16b,a#,1b" 

class Blinky:
	""" Just handle LED with blink state """
	FIXED = const( 0 )
	BLINK_SLOW = const( 500 ) # 500 ms
	BLINK_FAST = const( 200 ) # 200 ms

	def __init__( self, pin ):
		self.pin = pin
		self.off()

	def on( self ):
		self.interval = self.FIXED
		self.last_update = time.ticks_ms()
		self.pin.value( True )

	def off( self ):
		self.interval = self.FIXED
		self.last_update = time.ticks_ms()
		self.pin.value( False )

	def blink( self, fast=False ):
		self.interval = self.BLINK_FAST if fast else self.BLINK_SLOW
		self.last_update = time.ticks_ms() 
		self.pin.value( True )
		

	def update( self ):
		if self.interval == self.FIXED:
			return
		if time.ticks_diff( time.ticks_ms(), self.last_update ) < self.interval:
			return
		self.pin.toggle()
		self.last_update = time.ticks_ms()


# === Player 1 / Joueur 1 =================================
led1 = Blinky( Pin( Pin.board.GP28, Pin.OUT ) )
btn1 = Pin( Pin.board.GP19, Pin.IN, Pin.PULL_UP )
first_btn1 = None # first time btn1 was pressed
def btn1_pressed( obj ):
	global first_btn1
	if first_btn1==None:
		first_btn1 = time.ticks_ms()
btn1.irq( trigger=Pin.IRQ_FALLING, handler=btn1_pressed )

# === Player 2 / Joueur 2 =================================
led2 = Blinky( Pin( Pin.board.GP26, Pin.OUT ) ) 
btn2 = Pin( Pin.board.GP21, Pin.IN, Pin.PULL_UP )
first_btn2 = None
def btn2_pressed( obj ):
	global first_btn2
	if first_btn2==None:
		first_btn2 = time.ticks_ms()
btn2.irq( trigger=Pin.IRQ_FALLING, handler=btn2_pressed )

# === Other / Autre =======================================
# Start / Demarrer
btn_start = Pin( Pin.board.GP20, Pin.IN, Pin.PULL_UP )
# LED status / LED de Status
led_status = Blinky( Pin( Pin.board.GP27, Pin.OUT ) )
# Buzzer
buzzer = RingTonePlayer( Pin.board.GP13 )

# === Game / Jeux =========================================

# Start  ---> 
# buzzer.play_str( START_SONG ) 
# buzzer.play_str( WIN_SONG ) 
# buzzer.play_str( LOOSE_SONG ) 

# Start Button ? / Boutons Start ?
led_status.blink()
while btn_start.value()==1:
	led_status.update()
	time.sleep_ms(20)
led_status.off()

while True:
	# All LEDs on / Toutes LEDs allumées 
	led1.on()
	led2.on()
	led_status.on()

	# Init round / initialisation round
	wait_ms = randint( 3, 10 )*1000
	first_btn1 = None
	first_btn2 = None
	buzzer.play_str( START_SONG )

	# The round is starting / debut du round
	led1.off()
	led2.off()
	led_status.off()

	# Wait loop
	start_ms = time.ticks_ms()
	_led = None
	while time.ticks_diff( time.ticks_ms(), start_ms ) < wait_ms:
		time.sleep_ms(100)
		if (first_btn1!=None) or (first_btn2!=None):
			_led = led1 if first_btn1!= None else led2
			_led.on()
			buzzer.play_str( LOOSE_SONG ) # End of game
			break

	# Still running the game ? / Le jeux continue encore ?
	if (first_btn1==None) and (first_btn2==None):
		# Go Signal 
		buzzer.play_tone( 2500, 500 )

		# Wait the first player to press a button
		# Attendre le premier joueur qui presse son bouton
		while (first_btn1==None) and (first_btn2==None):
			time.sleep_ms( 20 )

		# We have a Winnner / Nous avons un gagnant
		if first_btn1==None:
			_led = led2
		elif first_btn2==None:
			_led = led1
		else:
			_led = led1 if first_btn1<first_btn2 else led2
		_led.on()
		buzzer.play_str( WIN_SONG )

	_led.blink()

	# Start Button ? / Boutons Start ?
	while btn_start.value()==1:
		_led.update()
		time.sleep_ms(20)
	_led.off()
