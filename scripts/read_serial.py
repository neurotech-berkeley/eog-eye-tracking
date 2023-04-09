#!/user/bin/env python3 

import csv
import serial
import asyncio 
import subprocess
import os
import serial_asyncio
import aioconsole
import subprocess
from datetime import datetime

DEVICE_NAME = 'ESP32'
DEVICE_MAC_ADDRESS = '40-f5-20-45-22-d2'
CONNECTION_TIMEOUT = 10

output = subprocess.run(["ls /dev/tty.*"], stdout=subprocess.PIPE, shell=True, text=True)
ports = output.stdout.split("\n")[:-1]
i = 0
print("\n>> Select UART/USB to read from:\n")
for port in ports:
    print("  ", i, ":", port)
    i += 1
index = int(input("\n>> "))
port = ports[index]
print("\nOK, opening", port)

serialPort = serial.Serial(port=port, baudrate=115200,
                           bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

now = datetime.now()
dt_string = now.strftime("%m-%d-%Y-%H:%M:%S")
print("date and time =", dt_string)
csvfilename = "data/{}.csv".format(dt_string)
print(csvfilename)

buffer = [0, 0, 0, 0, 0]
buffer_len = 5
current_sample_len = 0

blink_threshold = 900

csvfile = open(csvfilename, 'x')
fieldnames = ['millis', 'adc']
writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
writer.writeheader()

while serialPort:
    x = serialPort.readline()
    print("OUTPUT")
    print(x)
    millis, adc = str(x).split(" ") #[2:][:-5].split(" ") # adc is 0 to 1023

    print(millis, adc)
    writer.writerow({'millis': millis, 'adc': adc})

async def receive(reader):
    print("receiving...")
    while True:
        data = await reader.readuntil(b'\n')
        #print(f'(recv): {data.strip().decode()}')
        print(data.decode().strip())

async def send(writer):
    writer.write(b"Connection Initialized")
    stdin, _ = await aioconsole.get_standard_streams()
    async for line in stdin:
        data = line.strip()
        if not data:
            continue
        writer.write(line)
    
async def open_bluetooth_terminal(port, baudrate, input_type):
    print(port)
    reader, writer = await serial_asyncio.open_serial_connection(url=port, baudrate=baudrate)
    writer.write(b"connected")
    receiver = receive(reader)
    controller = run_controller(writer, input_type)
    await ayncio.wait([receiver, controller])

#if len(sys.argv) != 3:
#    print("Invalid arguments. Correct usage: python3 controller.py <port name> <input type> (0 for keyboard, 1 for joystick)")
#    sys.exit()
#
#loop = asyncio.get_event_loop()
#task = open_bluetooth_terminal(sys.argv[1], 115200, sys.argv[2])
#try:
#    loop.run_until_complete(task)
#    loop.close()
#    #while serialPort:
#    #    x = serialPort.readline()
#    #    millis, adc = str(x)[2:][:-5].split(" ") # adc is 0 to 1023
#
#    #    print(millis, adc)
#    #    writer.writerow({'millis': millis, 'adc': adc})
#except KeyboardInterrupt:
#    print("EXITING...")

