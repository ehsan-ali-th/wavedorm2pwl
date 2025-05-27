"""
    Filename: config.py
    ~~~~~~~~~~~~~~~~~~~~~~~
    This file contains the adjustable configuration parameters that is used
        by wavedrom2pwl.py script.
        
    Author: Dr. Ehsan Ali
    Author's email: ehssan.aali@gmail.com
    Last Update: May, 2025 
    Version: 0.1
"""

DEBUG = False
CLOCK_PERIOD = 10           # nano seconds (ns)
VOLTAGE_AMPLITUDE = 1.8     # volt
VOLTAGE_SOURCE_INDEX = 100  # Spice voltage source. 
"""
    VOLTAGE_SOURCE_INDEX: The converter generated PWL lines using voltage 
        sources starting from the index mentioned here. For example, if
        the index is 100 then the generated voltage sources are ad the 
        following:
        V100 vsource1 GND PWL(...)
        V101 vsource2 GND PWL(...)
        and so on.
"""
VERSION = 0.1
