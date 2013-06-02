import pygame
import serial

pygame.init()

clock = pygame.time.Clock()
serial = serial.Serial('/dev/rfcomm1',9600,timeout=1)
print(serial)
q = 0
id=0
lastXaxis = 0
lastYaxis = 0
try:
    while True :

        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done=True # Flag that we are done so we exit this loop
        
        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
            if event.type == pygame.JOYBUTTONDOWN:
                print("Joystick button pressed.")
            if event.type == pygame.JOYBUTTONUP:
                print("Joystick button released.")
        print(q)
        q = q + 1


        joystick = pygame.joystick.Joystick(id)
        joystick.init()

        name = joystick.get_name()
        
        print (name)

        buttons = joystick.get_numbuttons()

        axes = joystick.get_numaxes()
        print("Number of axes: {}".format(axes) )

        for i in range(axes):
            print ("Format axis {} = {}".format(i,joystick.get_axis(i)))

        Yaxis = int(joystick.get_axis(0)*2)
        Xaxis = int(joystick.get_axis(1)*2)

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
