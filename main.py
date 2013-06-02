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

import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('uart', metavar='uart', type=str, help='UART channel to robot')
parser.add_argument('--joy', dest='joystick_id', type=int, help='joystick id')
parser.add_argument('-d', dest='debug', action="store_true", default=False)

config = parser.parse_args()
print(config)

def signum(number):
    if(number == 0):
        return 0
    if(number < 0):
        return -1
    else:
        return 1

def dispatch_events():
    for event in pygame.event.get():
        pass

def get_joystick(id):
    joystick = pygame.joystick.Joystick(id)
    joystick.init()
    return joystick

def print_joystic_axis_status(joystick):
    if not config.debug :
        return 
    for i in range(joystick.get_numaxes()):
        print ("Format axis {} = {}".format(i,joystick.get_axis(i)))

def change_engine_speed_message(left_engine,right_engine):
    return "v{}\r{}\r".format(left_engine,right_engine).encode()

def decide_action(Xaxis,Yaxis):
    if(Xaxis == -1 and Yaxis == 0):
        return change_engine_speed_message(-255,-255)
    elif(Xaxis == -1 and Yaxis == 1):
        return change_engine_speed_message(-255,0)
    elif(Xaxis == 0 and Yaxis == 1):
        return change_engine_speed_message(-255,255)
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
    return change_engine_speed_message(0,0)

def show_axis_value(Xaxis,Yaxis):
    if not config.debug :
        return
    print ("X = {}, Y = {}".format(Xaxis,Yaxis))

def process_axis_value(Xaxis,Yaxis,lastXaxis,lastYaxis):
    show_axis_value(Xaxis,Yaxis)
    if (Xaxis != lastXaxis) or (Yaxis != lastYaxis):
        return decide_action(Xaxis,Yaxis)
    return b""

def show_recive_data(serial):
    if not config.debug:
        return
    print("odebrane {}".format(serial.readline()))

def show_sended_data(data):
    if not config.debug:
        return
    print("wysyłane {}".format(data)) 

def send_action(serial,action):
    serial.write(action)
    show_sended_data(action)
    show_recive_data(serial)

def create_serial() :
    return serial.Serial(config.uart,9600,timeout=1)

def process(serial):
    clock = pygame.time.Clock()
    lastXaxis = 0
    lastYaxis = 0
    try:
        while True :
            dispatch_events()
            joystick = get_joystick(config.joystick_id)
            Yaxis = signum(joystick.get_axis(0))
            Xaxis = signum(joystick.get_axis(1))
            #print_joystic_axis_status(joystick)
            action = process_axis_value(Xaxis,Yaxis,lastXaxis,lastYaxis)
            send_action(serial,action)
    
            lastXaxis = Xaxis
            lastYaxis = Yaxis
    
            clock.tick(10)
    except KeyboardInterrupt:
        pass
serial = create_serial()
process(serial)    
print ("bye!")
pygame.quit()
serial.close()
