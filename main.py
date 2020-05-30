#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, InfraredSensor
from pybricks.parameters import Port, Stop, Button

ev3 = EV3Brick()

motor = Motor(Port.B)
sensor = InfraredSensor(Port.S1)

shutdown = False
active = False

ev3.speaker.set_volume(100, which='_all_')
motor.reset_angle(20)
motor.run_target(500, 75, wait=True)

while shutdown == False:
    if Button.CENTER in ev3.buttons.pressed():
        shutdown = True

    if sensor.distance() < 35:
        motor.run_target(500, 0, wait=True)
        motor.run_target(500, 75, wait=True)
        if active == True:
            ev3.speaker.say("Goodbye")
            active = False
        else:
            ev3.speaker.say("Hello")
            active = True


motor.run_target(500, 20, wait=True)
print("Shutting down Brick")
