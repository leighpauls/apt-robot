import serial
import sys
import time

from serial.tools import list_ports

def main() -> None:

    port_options = [p.device for p in list_ports.comports()]
    print(port_options)

    with serial.Serial(sys.argv[1], 19200, timeout=0) as ser:
        while True:
            # Flush the buffer
            bytes_waiting = ser.in_waiting
            print(f"{bytes_waiting} bytes waiting")
            print(ser.read(bytes_waiting))

            time.sleep(0.1)

if __name__ == '__main__':
    main()
