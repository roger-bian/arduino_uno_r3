import sys
import time
import argparse
from telemetrix import telemetrix


# Callback data indices
CB_PIN_MODE = 0
CB_PIN = 1
CB_VALUE = 2
CB_TIME = 3

def the_callback(data):
    """
    A callback function to report data changes.
    This will print the pin number, its reported value and
    the date and time when the change occurred

    :param data: [pin, current reported value, pin_mode, timestamp]
    """
    date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data[CB_TIME]))
    print(f'Pin Mode: {data[CB_PIN_MODE]} Pin: {data[CB_PIN]} Value: {data[CB_VALUE]} Time Stamp: {date}')

def on(board, pin):
    print(f'{pin}: ON')
    board.digital_write(pin, 1)    
    

def off(board, pin):
    print(f'{pin}: OFF')
    board.digital_write(pin, 0)


def digital_in_pullup(board, pin):
    print(f'pulling up {pin}...')
    # set the pin mode
    board.set_pin_mode_digital_input_pullup(pin, the_callback)
    time.sleep(0.001)
    board.set_pin_mode_digital_output(pin)
    time.sleep(0.001)
    board.digital_write(pin, 0)
    time.sleep(0.001)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Telemetrix Digital Pin Example')
    parser.add_argument('--pins', type=int, nargs='+', default=[13])
    parser.add_argument('--double', action='store_true')
    parser.add_argument('--blink', action='store_true')
    args = parser.parse_args()
    
    # Initialize the Telemetrix board
    board = telemetrix.Telemetrix()


    # pull up pins
    for pin in args.pins:
        digital_in_pullup(board, pin)


    try:
        if args.blink:
            while True:
                if args.double:
                    for pin1, pin2 in zip(args.pins[:-2], args.pins[2:]):
                        on(board, pin1)
                        on(board, pin2)
                        time.sleep(0.5)
                        off(board, pin1)
                        off(board, pin2)
                        time.sleep(0.5)
                else:
                    for pin in args.pins:
                        on(board, pin)
                        time.sleep(0.5)
                        off(board, pin)
                        time.sleep(0.5)
        else:
            for pin in args.pins:
                on(board, pin)
            while True:
                time.sleep(1)
            
        
    except KeyboardInterrupt:
        print('Exiting...')
        for pin in args.pins:
            board.digital_write(pin, 0)    
        
        board.shutdown()
        sys.exit(0)