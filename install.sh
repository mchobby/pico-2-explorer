#!/bin/sh

# Install the files on a pico
if [ -z "$1" ]
  then
    echo "/dev/ttyACMx parameter missing!"
                exit 0
fi

CUR_DIR=`pwd`
LIB_DIR="/home/domeu/python/esp8266-upy"
PICO_LIB_DIR="/home/domeu/python/micropython-pico"


CUR_DIR=`pwd`
while :
do

clear
echo "Wait for Pico on $1..."
while [ ! -f /media/domeu/RP2350/INFO_UF2.TXT ]; do sleep 1; done
echo "Flashing MicroPython..."
cp /home/domeu/Téléchargements/upy-os/pico2/RPI_PICO2-20241025-v1.24.0.uf2 /media/domeu/RP2350/
echo "Wait Pico reboot on $1..."
while ! (ls $1 2>/dev/null) do sleep 1; done;


# Install the files on a MicroPython board
mpremote connect $1 fs mkdir lib
mpremote connect $1 fs mkdir tuto
mpremote connect $1 fs cp $LIB_DIR/LIBRARIAN/lib/maps.py :lib/
mpremote connect $1 fs cp $PICO_LIB_DIR/lib/servo.py :lib/
mpremote connect $1 mip install github:mchobby/upy-rtttl

# mpremote connect $1 fs cp main.py :
# mpremote connect $1 fs cp boot.py :

# copy tutoriels
mpremote connect $1 fs cp analog-ldr/analog-ldr.py :tuto/analog-ldr.py
mpremote connect $1 fs cp analog-pot/analog-pot.py :tuto/analog-pot.py
mpremote connect $1 fs cp analog-pot/analog-mean.py :tuto/analog-mean.py
mpremote connect $1 fs cp analog-pot/analog-10bits.py :tuto/analog-10bits.py
mpremote connect $1 fs cp analog-tmp36/analog-tmp36.py :tuto/analog-tmp36.py
mpremote connect $1 fs cp buzzer/pwm-buzzer.py :tuto/pwm-buzzer.py
mpremote connect $1 fs cp buzzer/pwm-buzzer-9bits.py :tuto/pwm-buzzer-9bits.py
mpremote connect $1 fs cp debounce/debounce.py :tuto/debounce.py
mpremote connect $1 fs cp debounce/nodebounce.py :tuto/nodebounce.py
mpremote connect $1 fs cp input-button/input-button.py :tuto/input-button.py
mpremote connect $1 fs cp music/music1.py :tuto/music1.py
mpremote connect $1 fs cp output-led/output-led.py :tuto/output-led.py
mpremote connect $1 fs cp pwm-led/pwm-led.py :tuto/pwm-led.py
mpremote connect $1 fs cp servo/servo-pot.py :tuto/servo-pot.py
mpremote connect $1 fs cp servo/servo-simple.py :tuto/servo-simple.py


# Set the MCU datetime
mpremote connect $1 rtc --set

mpremote connect $1 run board-checkup.py

echo " "
echo "Done!"
done