import pygame
import socketLib
pygame.init()
 
def main():
    pygame.display.set_caption('JoyStick Example')
    surface = pygame.display.set_mode((1, 1))
    clock = pygame.time.Clock()
 
    font = pygame.font.Font(None, 20)
    linesize = font.get_linesize()
    joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
    for joy in joysticks:
        joy.init()
 
    while True:
        msg = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
            elif event.type == pygame.JOYBUTTONDOWN:
                print(event.button)
                id = event.button
                if id == 0:
                    msg = "stop"
                elif id == 1:
                    msg = "attach"
                elif id == 2:
                    msg = "detach"
                elif id == 6:
                    msg = "agile"
            elif event.type == pygame.JOYAXISMOTION:
                print(event.axis, int(event.value * 100))
                id, val = event.axis, int(event.value * 100)
                stroke = str(id) + " " + str(val)
                msg = stroke
            elif event.type == pygame.JOYHATMOTION:
                print(event.hat, event.value)
                x, y = event.value[0], event.value[1]
                if y == 1:
                    msg = "forward"
                elif y == -1:
                    msg = "back"
        if not msg is None:
            session.write(msg)
            #session.read()
        
        
        #surface.fill((0,0,0))
 
 
        #pygame.display.flip()
        #clock.tick(20)
 
    pygame.quit()
session = socketLib.host(4219)
session.accept()
main()

'''
QUIT              none
ACTIVEEVENT       gain, state
KEYDOWN           key, mod, unicode, scancode
KEYUP             key, mod
MOUSEMOTION       pos, rel, buttons
MOUSEBUTTONUP     pos, button
MOUSEBUTTONDOWN   pos, button
JOYAXISMOTION     joy, axis, value
JOYBALLMOTION     joy, ball, rel
JOYHATMOTION      joy, hat, value
JOYBUTTONUP       joy, button
JOYBUTTONDOWN     joy, button
VIDEORESIZE       size, w, h
VIDEOEXPOSE       none
USEREVENT         code
'''