#!/usr/bin/env pybricks-micropython 

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, InfraredSensor, ColorSensor
from pybricks.parameters import Port, Stop, Button
from pybricks.media.ev3dev import SoundFile

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
manual = False
said = False

def switchLight():
    global light
    light = not light
    motor.run_target(500, 0, wait=True)
    motor.run_target(500, 75, wait=False)

def switchSound():
    global sound
    sound = not sound
    soundMotor.run_target(500, 65, wait=True)
    soundMotor.run_target(500, 0, wait=False)

ev3.speaker.set_volume(100, which='_all_')
motor.reset_angle(20)
soundMotor.reset_angle(0)
motor.run_target(500, 75, wait=True)

while shutdown == False:

    print("running")

    ''' finishing the programm '''
    if Button.LEFT_UP in infraredSensor.buttons(2):
        shutdown = True

    if Button.RIGHT_UP in infraredSensor.buttons(1):
        manual = True
    
    if Button.BEACON in infraredSensor.buttons(1):
        if said == True:
            pass
        elif manual == True:
            ev3.speaker.play_file(SoundFile.DETECTED)
            said = True
        else:
            ev3.speaker.play_file(SoundFile.ERROR)
            said = True
    else:
        said = False

    ''' manual mode '''
    while manual == True:
        if light == False:
            if Button.LEFT_UP in infraredSensor.buttons(1):
                switchLight()
        else:
            if Button.LEFT_DOWN in infraredSensor.buttons(1):
                switchLight()
        if Button.BEACON in infraredSensor.buttons(1):
            if said == True:
                pass
            elif manual == True:
                ev3.speaker.play_file(SoundFile.DETECTED)
                said = True
            else:
                ev3.speaker.play_file(SoundFile.ERROR)
                said = True
        else:
            said = False
        if Button.RIGHT_DOWN in infraredSensor.buttons(1):
            manual = False



    ''' controlling the light in the room '''
    if active == True and light == False:
        if colorSensor.ambient() < 20:
            switchLight()
    elif active == True and light == True:
        if colorSensor.ambient() > 30:
            switchLight()
    elif active == False and light == True:
        switchLight()

    ''' controlling the sound in the room '''
    if active == True and sound == False:
        switchSound()
    elif active == False and sound == True:
        switchSound()

    ''' controlling the room state '''
    if sensor.distance() < 35:
        if active == True:
            ev3.speaker.play_file(SoundFile.GOODBYE)
            active = False
        else:
            if colorSensor.ambient() < 20:
                switchLight()
            ev3.speaker.play_file(SoundFile.HELLO)
            active = True


motor.run_target(500, 20, wait=True)
ev3.speaker.say("Shutting down Brick")
