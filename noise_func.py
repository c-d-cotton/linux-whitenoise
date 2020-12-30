#!/usr/bin/env python3
import os
from pathlib import Path
import sys

__projectdir__ = Path(os.path.dirname(os.path.realpath(__file__)) + '/')

def stopsound():
    import subprocess
    if os.path.isfile('/tmp/linux-whitenoise/pids.txt'):
        with open('/tmp/linux-whitenoise/pids.txt', 'r') as f:
            pids = f.read().encode('latin-1').splitlines()
        for pid in pids:
            try:
                subprocess.call(['kill', pid])
            except Exception:
                None
        os.remove('/tmp/linux-whitenoise/pids.txt')
        
    
def playsound(length, soundname = 'pinknoise', killoldsound = True, fade = ['0', '0', '0:10'], delay = 0, printmins = True):
    import os
    import subprocess
    import time

    if not os.path.isdir('/tmp/linux-whitenoise/'):
        os.mkdir('/tmp/linux-whitenoise/')

    if killoldsound is True:
        stopsound()

    # -q prevents output
    # -n synth 10 soundname makes it play whitenoise for 10 seconds
    # fade h 0:10 0 0:11 increase gradually for 10 seconds at start and decrease gradually for 11 seconds at end
    # delay 5 prevent start of sound by 5 seconds
    playargs = ['play', '-q', '-n', 'synth', str(length), soundname, 'fade', 'h'] + fade + ['delay', str(delay)]

    p = subprocess.Popen(playargs)

    with open('/tmp/linux-whitenoise/pids.txt', 'a+') as f:
        f.write(str(p.pid) + '\n')

    if printmins is True:
        minutesremaining = int(length/60)
        while minutesremaining > 0:
            print('Sound length: ' + str(length) + '. Minutes remaining: ' + str(minutesremaining) + '.')
            minutesremaining = minutesremaining - 1
            time.sleep(60)
        


def playsound_ap():
    #Argparse:{{{
    import argparse
    
    parser=argparse.ArgumentParser()
    parser.add_argument("length", help = "in minutes", type = float)
    parser.add_argument("--soundname", default = 'pinknoise')
    parser.add_argument("--killoldsound", action = 'store_true')
    
    args=parser.parse_args()
    #End argparse:}}}

    playsound(args.length * 60, soundname = args.soundname, killoldsound = args.killoldsound)
    
def playconsecutivesounds(length1, length2 = 60 * 60 * 24, soundname1 = 'pinknoise', soundname2 = 'brownnoise', killoldsound = True, interval = 5):
    import time

    # need to delete the pid of this process since otherwise 
    with open('/tmp/linux-whitenoise/pids.txt', 'a+') as f:
        f.write(str(os.getpid()) + '\n')

    playsound(length = length1, soundname = soundname1, killoldsound = killoldsound)

    playsound(length = length2, soundname = soundname2, killoldsound = False, fade = ['0:10', '0', '0'], delay = length1 + interval)


def playconsecutivesounds_ap():
    #Argparse:{{{
    import argparse
    
    parser=argparse.ArgumentParser()
    parser.add_argument("length1", help = "in minutes", type = float)
    parser.add_argument("--length2", help = "in minutes", type = float, default = 60 * 60 * 24)
    parser.add_argument("--soundname1", default = 'pinknoise')
    parser.add_argument("--soundname2", default = 'brownnoise')
    parser.add_argument("--killoldsound", action = 'store_true')
    parser.add_argument("--interval", help = "in seconds", type = float, default = 5)
    
    args=parser.parse_args()
    #End argparse:}}}

    playconsecutivesounds(args.length1 * 60, length2 = args.length2 * 60, soundname1 = args.soundname1, soundname2 = args.soundname2, killoldsound = args.killoldsound, interval = args.interval)


# Examples:{{{1
# plays brown noise for 20 minutes:
# playsound(20 * 60, soundname = 'brownnoise', killoldsound = False)

# plays 12 seconds of pink noise followed by 24 hours of brown noise with standard fades
# playconsecutivesounds(12)
