import pygame
import serial

pygame.init()


config = {}

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

def prepar_message(left_engine,right_engine):
    return b"{}\r{}\r".format(left_engine,right_engine)

clock = pygame.time.Clock()
serial = serial.Serial('/dev/rfcomm1',9600,timeout=1)
print(serial)
lastXaxis = 0
lastYaxis = 0
done = true

try:
    while done :

        Yaxis = signum(joystick.get_axis(0))
        Xaxis = signum(joystick.get_axis(1))

        if (Xaxis != lastXaxis) or (Yaxis != lastYaxis):
            print ("X = {}, Y = {}".format(Xaxis,Yaxis))
            serial.write(b'v')
            
            to_send = b"0\r0\r"
            
            if(Xaxis == -1 and Yaxis == 0):
                to_send = b"-255\r-255\r"
            elif(Xaxis == -1 and Yaxis == 1):
                to_send = b"-255\r0\r"
            elif(Xaxis == 0 and Yaxis == 1):
                to_send = b"-255\r255\r"
            elif(Xaxis == 1 and Yaxis == 1):
                to_send = b"255\r0\r"
            elif(Xaxis == 1 and Yaxis == 0):
                to_send = b"255\r255\r"
            elif(Xaxis == 1 and Yaxis == -1):
                to_send = b"0\r255\r"
            elif(Xaxis == 0 and Yaxis == -1):
                to_send = b"255\r-255\r"
            elif(Xaxis == -1 and Yaxis == -1):
                to_send = b"0\r-255\r"
                
            serial.write(to_send)
            print("wysyłane {}".format(to_send))
            print("odebrane {}".format(serial.readline()))
            
            lastXaxis = Xaxis
            lastYaxis = Yaxis

        clock.tick(10)
except KeyboardInterrupt:
    pass

print ("bye!")
pygame.quit()
serial.close()
