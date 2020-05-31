#!/usr/bin/env pybricks-micropython 

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, InfraredSensor, ColorSensor
from pybricks.parameters import Port, Stop, Button
from pybricks.media.ev3dev import SoundFile

import os

ev3 = EV3Brick()

motor = Motor(Port.A)
soundMotor = Motor(Port.B)
infraredSensor = InfraredSensor(Port.S3)
colorSensor = ColorSensor(Port.S2)
sensor = InfraredSensor(Port.S1)

shutdown = False
active = False
light = False
sound = False
manualLight = False
manualSound = False
said = False
saidSound = False

def switchLight():
    global light
    light = not light
    motor.run_target(500, 0, wait=True)
    motor.run_target(500, 75, wait=False)

def switchSound():
    global sound
    sound = not sound
    soundMotor.run_target(500, 63, wait=True)
    soundMotor.run_target(500, 0, wait=False)

def manualSoundControlButtons():
    global saidSound
    ''' checking buttons for manual sound control '''
    if Button.BEACON in infraredSensor.buttons(2):
        if saidSound == True:
            pass
        elif manualSound == True:
            ev3.speaker.play_file(SoundFile.DETECTED)
            saidSound = True
        else:
            ev3.speaker.play_file(SoundFile.ERROR)
            saidSound = True
    else:
        saidSound = False

def manualLightControlButtons():
    global said
    ''' checking buttons for manual sound control '''
    if Button.BEACON in infraredSensor.buttons(1):
        if said == True:
            pass
        elif manualLight == True:
            ev3.speaker.play_file(SoundFile.DETECTED)
            said = True
        else:
            ev3.speaker.play_file(SoundFile.ERROR)
            said = True
    else:
        said = False

def soundControl():
    global active, sound
    ''' controlling the sound in the room '''
    if active == True and sound == False:
        switchSound()
    elif active == False and sound == True:
        switchSound()

def lightControl():
    global active, light
    ''' controlling the light in the room '''
    if active == True and light == False:
        if colorSensor.ambient() < 20:
            switchLight()
    elif active == True and light == True:
        if colorSensor.ambient() > 30:
            switchLight()
    elif active == False and light == True:
        switchLight()

def manualLightControl():
    global light, manualLight
    if light == False:
        if Button.LEFT_UP in infraredSensor.buttons(1):
            switchLight()
    else:
        if Button.LEFT_DOWN in infraredSensor.buttons(1):
            switchLight()
    if Button.RIGHT_DOWN in infraredSensor.buttons(1):
        manualLight = False

def manualSoundControl():
    global sound, manualSound
    if sound == False:
        if Button.LEFT_UP in infraredSensor.buttons(2):
            switchSound()
    else:
        if Button.LEFT_DOWN in infraredSensor.buttons(2):
            switchSound()

    if Button.RIGHT_DOWN in infraredSensor.buttons(2):
        manualSound = False

# system setup
ev3.speaker.set_volume(100, which='_all_')
motor.reset_angle(20)
soundMotor.reset_angle(0)
motor.run_target(500, 75, wait=True)

# main project loop
while shutdown == False:

    if manualLight == True and manualSound == True:
        ''' finishing the progamm '''
        if Button.LEFT_UP in infraredSensor.buttons(3):
            shutdown = True

        manualLightControl()
        manualSoundControl()

        manualLightControlButtons()
        manualSoundControlButtons()


    elif manualLight == True and manualSound == False:
        ''' finishing the programm '''
        if Button.LEFT_UP in infraredSensor.buttons(3):
            shutdown = True

        ''' setting manual mode for sound '''
        if Button.RIGHT_UP in infraredSensor.buttons(2):
            manualSound = True

        manualLightControl()
        
        manualLightControlButtons()
        manualSoundControlButtons()

        soundControl()


    elif manualLight == False and manualSound == True:
        ''' finishing the programm '''
        if Button.LEFT_UP in infraredSensor.buttons(3):
            shutdown = True

        ''' setting manual mode for light '''
        if Button.RIGHT_UP in infraredSensor.buttons(1):
            manualLight = True

        manualSoundControl()

        manualLightControlButtons()
        manualSoundControlButtons()

        lightControl()

    else:

        ''' finishing the programm '''
        if Button.LEFT_UP in infraredSensor.buttons(3):
            shutdown = True

        ''' setting manual mode for light '''
        if Button.RIGHT_UP in infraredSensor.buttons(1):
            manualLight = True

        ''' setting manual mode for sound '''
        if Button.RIGHT_UP in infraredSensor.buttons(2):
            manualSound = True

        manualLightControlButtons()
        manualSoundControlButtons()

        lightControl()
        soundControl()

        ''' controlling the room state '''
        if sensor.distance() < 35:
            if active == True:
                ev3.speaker.play_file(SoundFile.GOODBYE)
                active = False
            else:
                if colorSensor.ambient() < 20:
                    switchLight()
                switchSound()
                ev3.speaker.play_file(SoundFile.HELLO)
                active = True

if light == True:
    switchLight()
if sound == True:
    switchSound()

motor.run_target(500, 20, wait=True)
ev3.speaker.say("Shutting down Brick")
os.system("echo maker | sudo -S poweroff")
