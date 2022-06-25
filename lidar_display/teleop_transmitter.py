import pygame
import time

def main() -> None:
    pygame.init()
    pygame.joystick.init()

    print('joystcks:', pygame.joystick.get_count())

    if pygame.joystick.get_count() == 0:
        print('No joysticks found, exiting...')
        exit(1)

    js = joystick = pygame.joystick.Joystick(0)
    joystick.init()

    print("Joystick:", joystick.get_instance_id())
    print("name:", joystick.get_name())
    print("guid:", joystick.get_guid())
    print("axis:", joystick.get_numaxes())

    while True:
        for event in pygame.event.get(): # User did something.
            if event.type == pygame.QUIT: # If user clicked close.
                done = True # Flag that we are done so we exit this loop.
            elif event.type == pygame.JOYBUTTONDOWN:
                print(f"Joystick button pressed. Inst: {event.instance_id} Button: {event.button}")
            elif event.type == pygame.JOYBUTTONUP:
                print(f"Joystick button released. Inst: {event.instance_id} Button: {event.button}")
            elif event.type == pygame.JOYAXISMOTION:
                print(f"Joystick axis moved. Inst {event.instance_id} axis: {event.axis} value: {event.value}")
            elif event.type == pygame.JOYHATMOTION:
                print(f"Joystick hat moved. Inst {event.instance_id} axis: {event.hat} value: {event.value}")
            elif event.type == pygame.JOYBALLMOTION:
                print(f"Joystick ball moved. Inst {event.instance_id} axis: {event.ball} value: {event.rel}")
        time.sleep(0.1)

if __name__ == '__main__':
    main()
