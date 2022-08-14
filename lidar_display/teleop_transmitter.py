import pygame
import serial
import time
import sys

from serial.tools import list_ports

def main() -> None:

    port_options = [p.device for p in list_ports.comports()]
    print(port_options)

    pygame.init()
    pygame.joystick.init()

    print('joystcks:', pygame.joystick.get_count())

    if pygame.joystick.get_count() == 0:
        print('No joysticks found, exiting...')
        exit(1)

    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    print("Joystick:", joystick.get_instance_id())
    print("name:", joystick.get_name())
    print("guid:", joystick.get_guid())
    print("axis:", joystick.get_numaxes())

    with serial.Serial(sys.argv[1], 19200, timeout=0) as ser:
        while True:
            for event in pygame.event.get(): # User did something.
                if event.type == pygame.QUIT: # If user clicked close.
                    done = True # Flag that we are done so we exit this loop.
                # elif event.type == pygame.JOYBUTTONDOWN:
                #     print(f"Joystick button pressed. Inst: {event.instance_id} Button: {event.button}")
                # elif event.type == pygame.JOYBUTTONUP:
                #     print(f"Joystick button released. Inst: {event.instance_id} Button: {event.button}")
                # elif event.type == pygame.JOYAXISMOTION:
                #     print(f"Joystick axis moved. Inst {event.instance_id} axis: {event.axis} value: {event.value}")
                # elif event.type == pygame.JOYHATMOTION:
                #     print(f"Joystick hat moved. Inst {event.instance_id} axis: {event.hat} value: {event.value}")
                # elif event.type == pygame.JOYBALLMOTION:
                #     print(f"Joystick ball moved. Inst {event.instance_id} axis: {event.ball} value: {event.rel}")

            left = max(-100, min(100, round(100 * joystick.get_axis(1))))
            left_dir = '-' if left < 0 else ''

            right = -max(-100, min(100, round(100 * joystick.get_axis(3))))
            right_dir = '-' if right < 0 else ''

            command = bytes(f"CM{left_dir}{abs(left):03d} {right_dir}{abs(right):03d}\n", 'ascii')
            print(command)
            ser.write(command)

            # Flush the buffer
            bytes_waiting = ser.in_waiting
            print(f"{bytes_waiting} bytes waiting")
            ser.read(bytes_waiting)

            time.sleep(0.1)

if __name__ == '__main__':
    main()
