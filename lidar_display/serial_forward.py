import serial
import sys
import time

from serial.tools import list_ports

def main() -> None:

    port_options = [p.device for p in list_ports.comports()]
    print(port_options)

    with serial.Serial(sys.argv[1], 19200, timeout=0) as input_ser:
        with serial.Serial(sys.argv[2], 19200, timeout=0) as output_ser:
            while True:
                # Flush the buffers
                if input_bytes_waiting := input_ser.in_waiting:
                    # print(f'input: {input_bytes_waiting}')
                    output_ser.write(input_ser.read(input_bytes_waiting))

                if output_bytes_waiting := output_ser.in_waiting:
                    print(f'output: {output_bytes_waiting}')
                    input_ser.write(output_ser.read(output_bytes_waiting))

                # time.sleep(0.01)

if __name__ == '__main__':
    main()
