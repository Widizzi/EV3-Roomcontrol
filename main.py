#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, InfraredSensor, ColorSensor
from pybricks.parameters import Port, Stop, Button

ev3 = EV3Brick()

motor = Motor(Port.A)
infraredSensor = InfraredSensor(Port.S1)
colorSensor = ColorSensor(Port.S2)

shutdown = False
active = False
light = False

def switchLight():
    global light
    light = not light
    motor.run_target(500, 0, wait=True)
    motor.run_target(500, 75, wait=True)

ev3.speaker.set_volume(100, which='_all_')
motor.reset_angle(20)
motor.run_target(500, 75, wait=True)

while shutdown == False:
    if Button.CENTER in ev3.buttons.pressed():
        shutdown = True

    ''' controlling the light in the room '''
    if active == True and light == False:
        if colorSensor.ambient() < 20:
            switchLight()
    elif active == True and light == True:
        if colorSensor.ambient() > 30:
            switchLight()
    elif active == False and light == True:
        switchLight()

    ''' controlling the room state '''
    if infraredSensor.distance() < 35:
        if active == True:
            ev3.speaker.say("Goodbye")
            active = False
        else:
            if colorSensor.ambient() < 20:
                switchLight()
            ev3.speaker.say("Hello")
            active = True


motor.run_target(500, 20, wait=True)
print("Shutting down Brick")
