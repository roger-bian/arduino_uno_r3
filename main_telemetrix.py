import sys
import time
from telemetrix import telemetrix

# pins
DIGITAL_PIN = [
    3,
    4,
    5,
    6,
    9,
    10,
    11,
    12
]

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

def on_off_single(board, pin):
    print(f'{pin}: ON')
    board.digital_write(pin, 1)
    time.sleep(1)
    
    print(f'{pin}: OFF')
    board.digital_write(pin, 0)
    time.sleep(1)


def on_off_double(board, pin1, pin2):
    print(f'{pin1} & {pin2}: ON')
    board.digital_write(pin1, 1)
    board.digital_write(pin2, 1)
    time.sleep(1)
    
    print(f'{pin1} & {pin2}: OFF')
    board.digital_write(pin1, 0)
    board.digital_write(pin2, 0)
    time.sleep(1)


def digital_in_pullup(board, pin):
    print(f'pulling up {pin}...')
    # set the pin mode
    board.set_pin_mode_digital_input_pullup(pin, the_callback)
    time.sleep(0.001)
    board.set_pin_mode_digital_output(pin)
    time.sleep(0.001)
    board.digital_write(pin, 0)
    time.sleep(0.001)



board = telemetrix.Telemetrix(
    com_port="COM4",
    arduino_instance_id=1,
    # arduino_wait=2,
)


# pull up pins
for pin in DIGITAL_PIN:
    digital_in_pullup(board, pin)


try:
    while True:
        # single pin
        for pin in DIGITAL_PIN:
            on_off_single(board, pin)
            
            
        # double pin
        on_off_double(board, DIGITAL_PIN[0], DIGITAL_PIN[2])
        on_off_double(board, DIGITAL_PIN[1], DIGITAL_PIN[3])
        on_off_double(board, DIGITAL_PIN[2], DIGITAL_PIN[4])
        on_off_double(board, DIGITAL_PIN[3], DIGITAL_PIN[5])
        on_off_double(board, DIGITAL_PIN[4], DIGITAL_PIN[6])
        on_off_double(board, DIGITAL_PIN[5], DIGITAL_PIN[7])
        
    
except KeyboardInterrupt:
    print('Exiting...')
    for pin in DIGITAL_PIN:
        board.digital_write(pin, 0)    
    
    board.shutdown()
    sys.exit(0)