#!/usr/bin/env python

# README #
# This program is an example that reads from the SmartGlove and plots 
# the accelerometer data using matplotlib
# 
# The code should be compatible with Python 2 and potentially Python 3
#
# If you don't want to use matplotlib, remove the lines enclosed by:
#   ### REMOVE IF NOT USING MATPLOTLIB ###
#

# built in libraries
import argparse     
import json         
import sys
import traceback
import os
### REMOVE IF NOT USING MATPLOTLIB ###
# For Ubuntu or other linux distros:
#   sudo apt-get install python-matplotlib python-mpl_toolkits.basemap python-serial
# For Windows:
#   You might need to get modules from here: http://www.lfd.uci.edu/~gohlke/pythonlibs
#   Then install using: pip install <module_name>.whl
# For OS X:
#   I recommend using pip or homebrew to install

#import matplotlib as mpl 
#import matplotlib.pyplot as plt
# from mpl_tookits.mplot3d import Axes3D # this can't be found for some reason
#import importlib
#importlib.import_module('mpl_toolkits.mplot3d').Axes3D # this hack adds Axes3D
### REMOVE IF NOT USING MATPLOTLIB ###

import numpy as np
import serial

# this try-except block binds the 'raw_input' function to the 'input' function
# allowing the code to run using both python2 and python3
# to regain functionality of input in python2, comment out this block or use eval(input())
try:
    input = raw_input
except NameError:
    pass


# main function, takes arguments from command line
def main(argv):
    # parse input arguments
    parser = argparse.ArgumentParser(description="Read JSON from the SmartGlove via serial and plots the acceleromter data")
    parser.add_argument("-p", "--port", 
            required=True, type=str, 
            help="Specify serial port. Usually a COM* or /dev/tty* port.")
    parser.add_argument("-b", "--baud", 
            type=int, default=115200, 
            help="Baud rate of serial port. Default is 115200.")
    args = parser.parse_args()

    # try to open the serial port
    try:
        ser = serial.Serial(args.port, args.baud)
    except serial.SerialException:
        # if you can't open the serial port, make sure the Arduino IDE serial monitor is closed
        # you can find the correct serial port by looking at Tools->Port in the IDE
        print("Could not open serial port.")
        sys.exit(2)

### REMOVE IF NOT USING MATPLOTLIB ###
#    # setup the plot
#    mpl.interactive(True) # this allows real time updates to the plot
#    fig = plt.figure()
#    ax = fig.add_subplot(111, projection='3d')
#
#    # arrays for the accelerometer data
#    acx = np.zeros(25) 
#    acy = np.zeros(25)
#    acz = np.zeros(25)
#
#    # make the plot
#    sc = ax.plot(acx, acy, acz)
### REMOVE IF NOT USING MATPLOTLIB ###

    release = True;
    fout = open('motiondata', 'w');

    previous = 0;
    # main loop
    while True:
        try:
            # gets json data and decodes it for python3 compatibility
            glove_data = json.loads(ser.readline().decode('utf-8')) 
            #print(str(json.dumps(glove_data, indent=4, sort_keys=True))) # pretty print 
            
### REMOVE IF NOT USING MATPLOTLIB ###
            # update plot with accelerometer data by shifting it into the arrays
            #acx = np.append(acx[1:], glove_data["hand"]["accelerometer"]["g"]["x"])
            #acy = np.append(acy[1:], glove_data["hand"]["accelerometer"]["g"]["y"])
            #acz = np.append(acz[1:], glove_data["hand"]["accelerometer"]["g"]["z"])
            #sc = ax.plot(acx, acy, acz)
            #plt.draw() # update the plot
### REMOVE IF NOT USING MATPLOTLIB ###

        # catch CTRL+C for exit
        except KeyboardInterrupt:
            fout.close();
            print("Exiting.") 
            sys.exit(0) 
        # print exceptions and keep moving
        except:
            #traceback.print_exc()
            continue
        os.system('clear') 
        #print(str(json.dumps(glove_data, indent=4, sort_keys=True))) # pretty print 

        fout.write( str( glove_data["hand"]["accelerometer"]["adc"]["z"] ) );
        fout.write( '\n' );
        print("Roll " + str(glove_data["hand"]["attitude"]["degrees"]["roll"]));
        print("Pitch " + str(glove_data["hand"]["attitude"]["degrees"]["pitch"]));
        print("Heading " + str(glove_data["hand"]["attitude"]["degrees"]["heading"]));
        
        print("Accel");
        print(glove_data["hand"]["accelerometer"]["adc"]["x"]);
        print(glove_data["hand"]["accelerometer"]["adc"]["y"]);
        print(glove_data["hand"]["accelerometer"]["adc"]["z"]);
        previous = glove_data["hand"]["accelerometer"]["adc"]["z"];
        print("Flex");
        print(glove_data["fingers"]["flex"][0]);
        print(glove_data["fingers"]["flex"][1]);
        print(glove_data["fingers"]["flex"][2]);
        print(glove_data["fingers"]["flex"][3]);
        print(glove_data["fingers"]["flex"][4]);
        print("Pressure");
        print(glove_data["fingers"]["pressure"][0]);
        print(glove_data["fingers"]["pressure"][1]);
        print(glove_data["fingers"]["pressure"][2]);
        print(glove_data["fingers"]["pressure"][3]);
        print(glove_data["fingers"]["pressure"][4]);
        # wait for the user to update 
        #input("Press Any Key to Continue...")

# main
if __name__ == "__main__":
    main(sys.argv[1:]) 
