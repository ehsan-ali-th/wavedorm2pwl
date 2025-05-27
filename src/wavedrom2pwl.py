#!/usr/bin/env python

"""
    Filename: wavedrom2pwl.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    This is the main Python script that defines states and run a state
        machine to convert Wavedrom JSON to NGSpice PWL lines.
        
    Author: Dr. Ehsan Ali
    Author's email: ehssan.aali@gmail.com
    Last Update: May, 2025 
    Version: 0.1
    
    ---------------------------------------------------------------------------
    Usage: $python3 wavedrom2pwl.py wavedrom_input.json ngspice_output.txt
    
     where: - wavedrom2pwl.py is this file
            - wavedrom_input.json is a text file containing the Wavedrom JSON. 
                 To generate this file simply design your waveform in the
                 the Wavedrom editor and then copy and paste the generated
                 JSON text into 'wavedrom_input.json' file.
            -  ngspice_output.txt is the name of output file that will be
                generated and save in the working directory (the directory 
                where the Python script is invoked) if the conversion is
                successful.
     Notes:
            - The JSON input must contain valid JSON text.
            - ALL JSON input fields must be double quoted. Look at the
                provided wavedrom.json sample file.
"""

import json
import sys
from State import State
from StateMachine import StateMachine

from config import DEBUG
from config import CLOCK_PERIOD
from config import VOLTAGE_SOURCE_INDEX
from config import VOLTAGE_AMPLITUDE
from config import VERSION


class S_init(State):
    """
        Definition of the state: S_init
    """
    def run(self, t):
        if DEBUG:
            print("S_init")
        return "0n"
    def next(self, char):
        if char == '0':
            return Wavedorm2NGSpiceSM.s_0_init
        elif char == '1':
            return Wavedorm2NGSpiceSM.s_1_init
        elif char == '.':
            return Wavedorm2NGSpiceSM.s_init
        elif char == 'p':
            return Wavedorm2NGSpiceSM.s_pos_clk_init
        return Wavedorm2NGSpiceSM.s_0_init

class S_pos_clk_init(State):
    """
        Definition of the state: S_pos_clk_init
    """
    def run(self, t):
        if DEBUG:
            print("S_pos_clk_init")
        return ("," + str(VOLTAGE_AMPLITUDE) + 
                " ," + str(int((CLOCK_PERIOD / 2) + t))  + "n," + str(VOLTAGE_AMPLITUDE) + ", "
                     + str(int((CLOCK_PERIOD / 2) + t))  + "n," + "0, "
                     + str(int(CLOCK_PERIOD + t)) + "n,0")
    def next(self, char):
        if char == '.':
            return Wavedorm2NGSpiceSM.s_pos_clk
        else: 
            raise ValueError("Expecting character '.' in clock generation mode after 'p'")

class S_pos_clk(State):
    """
        Definition of the state: S_pos_clk_
    """    
    def run(self, t):
        if DEBUG:
            print("S_pos_clk")
        return (", " + str(t)  + "n," + str(VOLTAGE_AMPLITUDE)
                     +", " + str(int((CLOCK_PERIOD / 2) + t))  + "n," + str(VOLTAGE_AMPLITUDE) + ", "
                     + str(int((CLOCK_PERIOD / 2) + t))  + "n," + "0, "
                     + str(int(CLOCK_PERIOD + t)) + "n,0")
    def next(self, char):
        if char == '.':
            return Wavedorm2NGSpiceSM.s_pos_clk
        else: 
            raise ValueError("Expecting character '.' in clock generation mode after 'p'")

   
class S_0_init(State):
    """
        Definition of the state: S_0_init
    """
    def run(self, t):
        if DEBUG:
            print("s_0_init")
        return ",0"
    def next(self, char):
        if char == '0':
            return Wavedorm2NGSpiceSM.s_0_already
        elif char == '1':
            return Wavedorm2NGSpiceSM.s_1_already
        elif char == '.':
            return Wavedorm2NGSpiceSM.s_0_already
        return Wavedorm2NGSpiceSM.s_init

class S_1_init(State):
    """
        Definition of the state: S_1_init
    """
    def run(self, t):
        if DEBUG:
            print("s_1_init")
        return "," + str(VOLTAGE_AMPLITUDE)
    def next(self, char):
        if char == '0':
            return Wavedorm2NGSpiceSM.s_0_after_1
        elif char == '1':
            return Wavedorm2NGSpiceSM.s_1_already
        elif char == '.':
            return Wavedorm2NGSpiceSM.s_1_already
        return Wavedorm2NGSpiceSM.s_init

class S_0_already(State):
    """
        Definition of the state: S_0_already
    """
    def run(self, t):
        if DEBUG:
            print("S_0_already")
        return ""
    def next(self, char):
        if char == '0':
            return Wavedorm2NGSpiceSM.s_0_continues
        elif char == '1':
            return Wavedorm2NGSpiceSM.s_1_after_0
        elif char == '.':
            return Wavedorm2NGSpiceSM.s_0_continues
        return Wavedorm2NGSpiceSM.s_0_continues

class S_1_already(State):
    """
        Definition of the state: S_1_already
    """
    def run(self, t):
        if DEBUG:
            print("S_1_already")
        return ""
    def next(self, char):
        if char == '0':
            return Wavedorm2NGSpiceSM.s_0_after_1
        elif char == '1':
            return Wavedorm2NGSpiceSM.s_1_continues
        elif char == '.':
            return Wavedorm2NGSpiceSM.s_1_continues
        return Wavedorm2NGSpiceSM.s_1_continues

class S_0_continues(State):
    """
        Definition of the state: S_0_continues
    """
    def run(self, t):
        if DEBUG:
            print("S_0_continues")
        return ""
    def next(self, char):
        if char == '0':
            return Wavedorm2NGSpiceSM.s_0_continues
        elif char == '1':
            return Wavedorm2NGSpiceSM.s_1_after_0
        elif char == '.':
            return Wavedorm2NGSpiceSM.s_0_continues
        return Wavedorm2NGSpiceSM.s_0_already

class S_1_continues(State):
    """
        Definition of the state: S_1_continues
    """
    def run(self, t):
        if DEBUG:
            print("S_1_continues")
        return ""
    def next(self, char):
        if char == '0':
            return Wavedorm2NGSpiceSM.s_0_after_1
        elif char == '1':
            return Wavedorm2NGSpiceSM.s_1_continues  
        elif char == '.':
            return Wavedorm2NGSpiceSM.s_1_continues
        return Wavedorm2NGSpiceSM.s_1_already

class S_1_after_0(State):
    """
        Definition of the state: S_1_after_0
    """
    def run(self, t):
        if DEBUG:   
            print("S_1_after_0")
        return (" ," + str(int((CLOCK_PERIOD / 2) + t))  + "n," + "0, "
                     + str(int((CLOCK_PERIOD / 2) + t))  + "n," + str(VOLTAGE_AMPLITUDE) + ", "
                     + str(int(CLOCK_PERIOD + t)) + "n," + str(VOLTAGE_AMPLITUDE))
    def next(self, char):
        if char == '0':
            return Wavedorm2NGSpiceSM.s_0_after_1
        elif char == '1':
            return Wavedorm2NGSpiceSM.s_1_continues  
        elif char == '.':
            return Wavedorm2NGSpiceSM.s_1_continues
        return Wavedorm2NGSpiceSM.s_1_already

class S_0_after_1(State):
    """
        Definition of the state: S_0_after_1
    """
    def run(self, t):
        if DEBUG:
            print("S_0_after_1")
        return (" ," + str(int((CLOCK_PERIOD / 2) + t)) + "n," + str(VOLTAGE_AMPLITUDE) + ", " 
                     + str(int((CLOCK_PERIOD / 2) + t)) + "n," + "0, " 
                     + str(int(CLOCK_PERIOD + t)) + "n,0")
    def next(self, char):
        if char == '0':
            return Wavedorm2NGSpiceSM.s_0_continues
        elif char == '1':
            return Wavedorm2NGSpiceSM.s_1_after_0
        elif char == '.':
            return Wavedorm2NGSpiceSM.s_0_continues
        return Wavedorm2NGSpiceSM.s_0_already


class Wavedorm2NGSpiceSM(StateMachine):
    """
        Definition of the state machine. The initial state is set to 
            'Wavedorm2NGSpiceSM.s_init'
    """
    def __init__(self):
        # Initial state
        StateMachine.__init__(self, Wavedorm2NGSpiceSM.s_init)

"""
    Static variable initialization.
"""
Wavedorm2NGSpiceSM.s_init           = S_init()
Wavedorm2NGSpiceSM.s_pos_clk_init   = S_pos_clk_init()
Wavedorm2NGSpiceSM.s_pos_clk        = S_pos_clk()
Wavedorm2NGSpiceSM.s_0_init         = S_0_init()
Wavedorm2NGSpiceSM.s_1_init         = S_1_init()
Wavedorm2NGSpiceSM.s_0_already      = S_0_already()
Wavedorm2NGSpiceSM.s_1_already      = S_1_already()
Wavedorm2NGSpiceSM.s_0_continues    = S_0_continues()
Wavedorm2NGSpiceSM.s_1_continues    = S_1_continues()
Wavedorm2NGSpiceSM.s_1_after_0      = S_1_after_0()
Wavedorm2NGSpiceSM.s_0_after_1      = S_0_after_1()


def convert_to_bitin(json_file, output_file, clock_period=10):
    """
        The convert_to_bitin function receives an input filename and then
            opens it to read JSON text. It then converts the JSON text if
            it is a valid JSON content. Then generated spice PWL lines 
            is written into output_file filename. The default clock period
            is 10ns unless another clock period is passed to the function.
            
        Parameters: 
           json_file: The input filename containing Wavedrom JSON
           output_file: The output filename 
           clock_period: Clock period with default value = 10ns
           
        Global variables:
            VOLTAGE_SOURCE_INDEX: used to append an arbitrary number to 
                Spice voltage source instance names, e.g., V100, V101, etc.
    """
    output_file_content = ""
    with open(json_file, 'r') as f:
        content = f.read()
        if DEBUG:
            print("Input file content:")
            print (content)
            print("Input file content ends.")
        f.seek(0)
        data = json.load(f)
        if DEBUG:
            print (data)
            print("data array size = ", len(data))
        signal = data['signal']
        print("signal array size = ", len(signal))
        for i, sig in enumerate(signal):
            pwl = process_wave(signal[i]['wave'])
            output_file_line = "V" + str(int(VOLTAGE_SOURCE_INDEX + i)) + " " + signal[i]['name'] + " GND " + pwl 
            print(output_file_line)
            output_file_content =  output_file_content + output_file_line + "\n"
    with open(output_file, 'w') as f:
        try:
            f.write(output_file_content)
            print("Writing PWLs into " + output_file + " = successful.")
        except FileNotFoundError:
            print("Error: File not found.")
        except PermissionError:
            print("Error: Permission denied.")
        except IsADirectoryError:
            print("Error: Is a directory.")
        except IOError as e:
            print(f"Error: Input/output error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            
def process_wave (wave, clock_period=10):
    """
        The process_wave function receives a 'wave' field from Wavedrom JSON
            and converts it into a PWL line.
            
        Parameters: 
            wave: A series of characters containing 0s and 1s to represent
                digital logic pulses recognized by the Wavedrom editor.
            clock_period: Clock period with default value = 10ns
            
        Global variables:
            VERSION: The script version just to make this conversion tool 
                to look cool. Software without version does not look cool.
    """
    print("Converting the following bits to NGSpice PWL:")
    wave_characters = list (wave)
    i = 0
    pwl = "pwl ("
    time = 0
    prev_bit = 0
    for char in wave_characters:
        print(char+" ", end="")
        try:
            W2NG_SM = Wavedorm2NGSpiceSM()
            pwl = W2NG_SM.runAll(wave_characters)
        except Exception as error:
            print('Error #7001: ' + repr(error))
            sys.exit()
    print("\nConversion is done.")
    return pwl

print("Wavedrom JSON to NGSpice bit converter. Version: " + str(VERSION))
print("Author: Dr. Ehsan Ali - 2025")
print("Author's email: ehssan.aali@gmail.com")

if len(sys.argv) < 2:
    print("Usage: $python3 wavedrom2pwl.py wavedrom_input.json ngspice_output.txt")
    sys.exit()

wavedormFile = sys.argv[1]
ngspiceFile = sys.argv[2]

if DEBUG:
    print("wavedormFile =", wavedormFile)
    print("ngspiceFile =", ngspiceFile)

convert_to_bitin(wavedormFile, ngspiceFile)



