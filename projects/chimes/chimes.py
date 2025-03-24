from micropython import const
from machine import RTC
from rtplay import *
import time

HOUR_CHIME = const( 1 )
HALF_HOUR_CHIME = const( 2 )

rtc = RTC()
buzzer = RingTonePlayer( Pin.board.GP13 )

def next_chime( _now ):
    """  Calculate Next 1/2 H and Next Hour chimes time

     Parameters:
        _now : rtc datetime  (Y,M,D,wD,h,m,s,ms)
     
     returns:
        Time in seconds (since Jan 1, 2000), chime_type, related_hour
    """
    # mktime datetime (Y,M,D,h,m,s,wD,yD)
    if _now[5]<30: # Minutes < 30 => Chimes at next 30 mins
        mktime_data = ( _now[0], _now[1], _now[2], _now[4], 30, 0, _now[3], 0 )
        chime_type = HALF_HOUR_CHIME
        hour = _now[4]
    else: # Shime next Hour
        chime_type = HOUR_CHIME
        if _now[4]+1 > 23: # > 23H
            # Next day at 00:00
            # Transform in seconds
            mktime_data = ( _now[0], _now[1], _now[2], _now[4], _now[5], _now[6], _now[3], 0 )
            secs = time.mktime( mktime_data )
            # Add a day
            next_day_secs = secs + 24*60+60 + 30
            # Decode this new date
            mktime_data = time.localtime( next_day_secs )
            # Zeroing the Hours, Minutes (shime the at first second)
            mktime_data = ( mktime_data[0], mktime_data[1], mktime_data[2], 0, 0, 1, 0, 0 )
            hour = 0
        else:
            # Next Hour & Zeroing minutes, seconds
            mktime_data = ( _now[0], _now[1], _now[2], _now[4]+1, 0, 0, 0, 0 )
            hour = _now[4]+1
    
    # Return seconds, Half or full Hour chime, related Hour
    return time.mktime( mktime_data ), chime_type, hour


_now = rtc.datetime()
_next_chime_secs, _chime_type, _hour = next_chime( _now )

in_day_time = lambda hour : 7 <= hour <= 21

while True:
    # rtc datetime (Y,M,D,wD,h,m,s,ms)
    _now = rtc.datetime()
    # mktime datetime (Y,M,D,h,m,s,wD,yD)
    _mktime_data = ( _now[0], _now[1], _now[2], _now[4], _now[5], _now[6], _now[3], 0 )
    _now_secs = time.mktime( _mktime_data ) # Secs since Jan 1, 2000
    
    print( "Now = %r (%i secs)" % ( _now, _now_secs ) )
    print( "Chime at %i secs" % _next_chime_secs )
    print( "Chime time = %r " % ( time.localtime( _next_chime_secs ), ) )
    print( "-" * 40 )
    
    # It is time to play a Chime 
    if _now_secs > _next_chime_secs:
        if in_day_time( _hour ):
            if _chime_type == HOUR_CHIME:
                buzzer.play_str( "We'reRea:d=4,o=6,b=140:8d,8d,8e,8e,f,e,2p,2e,8d,8d,8e,8e,f,e,8d,8d,8e,8f,2p,8d5,16p,8d5,16p,16d5,32d5,32d5,8f,8p,8d,8p,8d5,16p,8d5,16p,16d5,32d5,32d5,8f,8d,8d,8a,8d5,16p,8d5,16p,16d5,16d5,8f,8p,8d" )
                time.sleep( 2 )
                for i in range( _hour if _hour < 13 else _hour-12 ):
                    buzzer.play_tone( 1500, 200 )
                    time.sleep_ms( 800 )
            else: # Half-Hour
                buzzer.play_str( "SexyEyes:d=16,o=6,b=125:b5,8p,32b5,32p,b5,p,32b5,p,32p,f#,8p,32f#,32p,f#,p,f#,p,e,8p,32e,32p,e,p,32e,p,32p,g#,8p,32g#,32p,g#,p,g#,p,f#6,8p,32f#,32p,f#,p,32f#,p,32p,a#,8p,32a#,32p,a#6,p,32a#,p,32p,b,8p,32b" )
        # Calculate time of the next chime 
        _next_chime_secs, _chime_type, _hour = next_chime( _now )
          
    time.sleep( 5 )