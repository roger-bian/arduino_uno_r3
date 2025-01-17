import pyfirmata
import time

board = pyfirmata.Arduino('COM4')

board.digital[13].mode = pyfirmata.OUTPUT # Set the digital pin 13 as output

try:
    while True:
        print('ON')
        board.digital[13].write(1)  # Set the digital pin 13 to high
        time.sleep(1)
        print('OFF')
        board.digital[13].write(0)  # Set the digital pin 13 to low
        time.sleep(1)
    
except Exception as err:
    print(err)
    
finally:
    print('OFF')
    board.digital[13].write(0)
    board.exit()