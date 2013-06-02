"""
    This program is driver for robot using pad connect to computer.
    Use UART-like bridge to robot (eg. bluetooth).

    Copyright (C) 2013 Łukasz "BamBucha" Dubiel <bambucha14@gmail.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import pygame
import serial

pygame.init()


config = { "uart" : "/dev/rfcomm1" }

def signum(number):
    if(number == 0):
        return 0
    if(number < 0):
        return -1
    else:
        return 1

def dispatch_events():
    for event in pygame.event.get(): 
        if event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
        if event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")

def get_joystick(id):
    joystick = pygame.joystick.Joystick(config.joystick_id)
    joystick.init()
    return joystick

def print_joystic_axis_status(joystick):
    for i in range(joystick.get_numaxes()):
        print ("Format axis {} = {}".format(i,joystick.get_axis(i)))

def prepar_engine_speed(left_engine,right_engine):
    return b"{}\r{}\r".format(left_engine,right_engine)

def change_engene_speed_message(left_engine,right_engine):
    return b"v" + prepar_engine_speed(left_engine,right_engine)

def decide_action(Xaxis,Yaxis):
    if(Xaxis == -1 and Yaxis == 0):
        return change_engine_speed_message(-255,-255)
    elif(Xaxis == -1 and Yaxis == 1):
        return change_engine_speed_message(-255,0)
    elif(Xaxis == 0 and Yaxis == 1):
        return  change_engine_speed_message(-255,255)
    elif(Xaxis == 1 and Yaxis == 1):
        return change_engine_speed_message(255,0)
    elif(Xaxis == 1 and Yaxis == 0):
        return change_engine_speed_message(255,255)
    elif(Xaxis == 1 and Yaxis == -1):
        return change_engine_speed_message(0,255)
    elif(Xaxis == 0 and Yaxis == -1):
        return change_engine_speed_message(255,-255)
    elif(Xaxis == -1 and Yaxis == -1):
        return change_engine_speed_message(0,-255)
    else :
        return change_engine_speed_message(0,0)

def process_axis_value(Xaxis,Yaxis,lastXaxis,lastYaxis):
    if (Xaxis != lastXaxis) or (Yaxis != lastYaxis):
        print ("X = {}, Y = {}".format(Xaxis,Yaxis))
        return decide_action(Xaxis,Yaxis)

def send_action(serial,action):
    serial.write(action)
    print("wysyłane {}".format(action)) 
    print("odebrane {}".format(serial.readline()))


def create_serial() :
    return serial.Serial(config.uart,9600,timeout=1)

def process(serial):
    clock = pygame.time.Clock()
    lastXaxis = 0
    lastYaxis = 0
    try:
        while True :
            joystick = get_joystick()
            Yaxis = signum(joystick.get_axis(0))
            Xaxis = signum(joystick.get_axis(1))
            
            action = process_axis_value(Xaxis,Yaxis,lastXaxis,lastYaxis)
            send_action(serial,action)
    
            lastXaxis = Xaxis
            lastYaxis = Yaxis
    
            clock.tick(10)
    except KeyboardInterrupt:
        pass

process(create_serial())    
print ("bye!")
pygame.quit()
serial.close()
