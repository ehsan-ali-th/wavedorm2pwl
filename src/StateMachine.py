#!/usr/bin/env python

"""
    Filename: StateMachine.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Defines StateMachine class.
        
    Author: Dr. Ehsan Ali
    Author's email: ehssan.aali@gmail.com
    Last Update: May, 2025 
    Version: 0.1
    
"""

from config import DEBUG

class StateMachine:
    """
        Represents a state machine.
    """
    NSSpiceCode = "pwl("
    clock_period = 10
    time = 0
    def __init__(self, initialState):
        self.currentState = initialState
        self.NSSpiceCode = self.NSSpiceCode + self.currentState.run(self.time)
    def runAll(self, inputs):
        """
            Runs the state machine through all the states according to the 
                inputs.
                
            Parameters:
                inputs: The Wavedrom JSON's 'wave' field containing 
                    the following valid characters: 'p', '0', '1', '.' 

            Returns:
                NSSpiceCode: A string that contains all PWLs lines.    
        """
        for i in inputs:
            if DEBUG:
                print(i)
            self.currentState = self.currentState.next(i)
            self.NSSpiceCode = self.NSSpiceCode + self.currentState.run(self.time)
            self.time = self.time + self.clock_period
        self.NSSpiceCode = self.NSSpiceCode + ")"
        if DEBUG:
            print(self.NSSpiceCode)
        return self.NSSpiceCode    
