import csv
import serial
import subprocess
from datetime import datetime

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
    millis, adc = str(x)[2:][:-5].split(" ") # adc is 0 to 1023

    print(millis, adc)
    writer.writerow({'millis': millis, 'adc': adc})
