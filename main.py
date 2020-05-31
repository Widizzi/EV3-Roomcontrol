#!/usr/bin/env pybricks-micropython 

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, InfraredSensor, ColorSensor, TouchSensor
from pybricks.parameters import Port, Stop, Button, Color
from pybricks.media.ev3dev import SoundFile
from pybricks.tools import wait, StopWatch

import os

ev3 = EV3Brick()
watch = StopWatch()

motor = Motor(Port.A)
soundMotor = Motor(Port.B)
sensor = InfraredSensor(Port.S1)
colorSensor = ColorSensor(Port.S2)
infraredSensor = InfraredSensor(Port.S3)
touchSensor = TouchSensor(Port.S4)

# true when ev3 is forced to shutdown
shutdown = False
# room state
active = False
# light state
light = False
# sound state
sound = False
# true if manual mode is active
manualLight = False
manualSound = False
# beacon button is toggle. To supress repetition in the loop these booleans will turn true after the first execution 
said = False
saidSound = False

# turns on or off the light physically
def switchLight():
    global light
    light = not light
    motor.run_target(500, 0, wait=True)
    motor.run_target(500, 75, wait=False)

# turn on or off the sound physically
def switchSound():
    global sound
    sound = not sound
    soundMotor.run_target(500, 63, wait=True)
    soundMotor.run_target(500, 0, wait=False)

# reads remote inputs and sets the corresponding variable (sound part)
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

# reads remote inputs and sets the corresponding variable (light part)
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

# controls the autonomous sound changes
def soundControl():
    global active, sound
    ''' controlling the sound in the room '''
    if active == True and sound == False:
        switchSound()
    elif active == False and sound == True:
        switchSound()

# controls the autonomous light changes
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

# controlls the manual light changes on button presses
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

# controlls the manual sound changes on button presses
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
ev3.light.on(Color.GREEN)
watch.reset()

# main project loop
while shutdown == False:

    ''' finishing the progamm '''
    if Button.LEFT_UP in infraredSensor.buttons(4):
        shutdown = True

    ''' checking touch sensor '''
    if touchSensor.pressed() == True:
        if manualLight == False and manualSound == False:
            manualLight = True
            manualSound = True
        else:
            manualLight = False
            manualSound = False
        wait(200)

    if manualLight == True and manualSound == True:

        ev3.light.on(Color.RED)

        manualLightControl()
        manualSoundControl()

        manualLightControlButtons()
        manualSoundControlButtons()


    elif manualLight == True and manualSound == False:

        ev3.light.on(Color.YELLOW)

        ''' setting manual mode for sound '''
        if Button.RIGHT_UP in infraredSensor.buttons(2):
            manualSound = True

        manualLightControl()
        
        manualLightControlButtons()
        manualSoundControlButtons()

        soundControl()


    elif manualLight == False and manualSound == True:

        ev3.light.off()

        ''' setting manual mode for light '''
        if Button.RIGHT_UP in infraredSensor.buttons(1):
            manualLight = True

        manualSoundControl()

        manualLightControlButtons()
        manualSoundControlButtons()

        lightControl()

    else:

        ev3.light.on(Color.GREEN)

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
        if watch.time() > 7000:
            if sensor.distance() < 35:
                watch.reset()
                if active == True:
                    ev3.speaker.play_file(SoundFile.GOODBYE)
                    active = False
                else:
                    if colorSensor.ambient() < 20:
                        switchLight()
                    switchSound()
                    ev3.speaker.play_file(SoundFile.HELLO)
                    active = True

# this part of code is executed after shutdown is initialized
if light == True:
    switchLight()
if sound == True:
    switchSound()

motor.run_target(500, 20, wait=True)
ev3.speaker.say("Shutting down Brick")

# this command shuts down the ev3
os.system("echo maker | sudo -S poweroff")
