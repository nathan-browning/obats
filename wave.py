import socket
import serial
import time
from time import sleep
from datetime import datetime

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

# main function
def main():
    # open file to potentially write input to
    f1 = open("input.txt", "w")
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # find and connect to serial port connected to GPS
    # gps = serial.Serial('../../../../dev/ttyACM0', baudrate = 9600, timeout = 0.5)      # ../../dev/ttyACM0 from home folder (type cd in command line)
    
    print("CPU time, GPS time, latitude(latitude direction), longitude(longitude direction), CPU date, altitude")
    print("\n")
    print("START DATA:")

    while 1:
        time.sleep(0.5)

        # data = gps.readline()
        test_str = "17:33:10,21:33:04,39 deg 46.81767 min(N),086 deg 11.52896 min(W),22/04/21,257.6 m"
        print(test_str)
        # print(len(test_str))
        sock.sendto(test_str.encode(), (UDP_IP, UDP_PORT))

        # parseGPS(data, sock)

# convert the data in the NMEA message into a easy-to-read format
def parseGPS(data, socket):
    data_str = str(data)                                    # convert data to a string
    key1 = "$GNGGA"                                         # GP signifies a satellite from the US network
    key2 = "$GPGGA"                                         # GN signifies a satellite from the Russian network

    if data_str.find(key1) > 0 or data_str.find(key2) > 0:  # find right NMEA message
        # print out the original NMEA string
        # print(data_str)

        sdata = data_str.split(",")                         # parse
        for x in range(0,9):
            if sdata[x] == "":
                bad_data_str = "INCOMPLETE DATA"
                print(bad_data_str)
                return

        if sdata[6] == '0':
            no_sat_str = "NO SATELLITE DATA AVAILABLE"
            print(no_sat_str)                                                       # print binary string
            return
        
        # parse the RMC message
        time = sdata[1][0:2] + ":" + sdata[1][2:4] + ":" + sdata[1][4:6]    # time
        lat = decode(sdata[2])                                              # latitude
        dirLat = sdata[3]                                                   # N/S
        lon = decode(sdata[4])                                              # longitude
        dirLon = sdata[5]                                                   # E/W
        alt = sdata[9]

        # get the curretnt time and date from microcontroller
        # note: there is a consistent five hour difference between CPU and GPS
        curTime = str(datetime.now())
        scurTime = curTime.split(" ")
        cpuTime = scurTime[1][0:8]                                                              # formatting CPU time to match GPS time
        cpuDate = scurTime[0][8:10] + "/" + scurTime[0][5:7] + "/" + scurTime[0][2:4]           # formatting CPU date to match GPS date

        # display all the data
        output_str = cpuTime + "," + time + "," + lat + "(" + dirLat + ")," + lon + "(" + dirLon + "),"  +  cpuDate + "," + alt + " m"
        # print out the string
        print(output_str)                                                                       # print out string
        
        # display length of string (for setting up udp socket in GNU Radio)
        # print(len(output_str))

        socket.sendto(output_str.encode(), (UDP_IP, UDP_PORT))                                  # use encode to convert to 'bytes-like' object
        sleep(0.1)

def decode(coord):
    # converts DDMM.MMMMM > DD deg MM.MMMMM
    x = coord.split(".")
    head = x[0]
    tail = x[1]
    deg = head[0:-2]
    minimum = head[-2:]
    return deg + " deg " + minimum + "." + tail + " min"

# write data to file
def readDataToFile(user_input):
    # open file in read-only mode
    f1 = open("input.txt", "r")

    content = f1.read()                         # get data from file
    split_content = content.split()             # split data from file into lines

    counter = 0

    # count the number of lines
    for i in split_content:
        if i:
            counter += 1

    print("the number of lines in the file:")
    print(counter)

    f1.close()
    
    # if there is 100 lines already, clear file, and start at top. Otherwise, append
    if counter >= 100:
        f1 = open("input.txt", "w")             # open in write mode (overwrites current data in file)
    else:
        f1 = open("input.txt", "a")             # open in append mode (adds data at end of file)

    f1.write(user_input)                        # write data
    f1.write("\n")                              # add newline

    f1.close()

# calling the main function
if __name__ == "__main__":
    main()
