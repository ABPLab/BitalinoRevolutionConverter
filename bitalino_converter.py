# -*- coding: utf-8 -*-
"""
BITalino Analogic-To-Digital Converter
This script act as a converter for Bitalino's Revolution collected Data.

Created on Wed Nov  8 19:25:01 2017

@author: giulio
"""

###############################################################################
#                                                                             #
#                                Libraries                                    #
#                                                                             #
###############################################################################
""" 

"""

import os #used for reading files and directories
import csv #used to handle csv data files
import matplotlib.pyplot as plt #plotting
import numpy as np #handle arrays and maths
import pickle #to open and save pkl files

###############################################################################
#                                                                             #
#                             PARAMETERS                                      #
#                                                                             #
###############################################################################

""" PATHS """ 
basepath = os.path.dirname(os.path.realpath(__file__)) #This get the basepath of the script

###############################################################################
#                                                                             #
#                               Functions                                     #
#                                                                             #
###############################################################################
def ecgconverter(rawECGSignal,VCC=3.3,nBits=10):
    """ Input: Bitalino's raw ECG signal as list
                VCC in Volt, default 3.3
                nBits, number of bits, can be 10 or 6
        Output: ECG signal in mV
    NOTE: output should be in range -1.5mV - 1.5mV
    """
    #http://bitalino.com/datasheets/REVOLUTION_ECG_Sensor_Datasheet.pdf
    gain = 1100 #sensor gain as defined in Data Sheet
    rawECGSignal = [ (((ADC / 2**nBits) - (1/2))*VCC ) / gain for ADC in rawECGSignal] #Apply the conversion, signal in V
    rawECGSignal = [value*1000 for value in rawECGSignal] #conversion to mV
    return(rawECGSignal)
    
def edaconverter(rawEDASignal,VCC=3.3,nBits=10):
    """
        Input: BITalino raw data in collected using Python API
                VCC in Volt, default 3.3
                nBits, number of bits, can be 10 or 6
        Output: EDA raw signal in uS
        
    NOTE: output should be in range -4.4uS - 21uS. If 
    """
    #http://bitalino.com/datasheets/REVOLUTION_EDA_Sensor_Datasheet.pdf
    rawEDASignal = [(((ADC / (2**nBits)) * VCC) - 0.574 ) / 0.132 for ADC in rawEDASignal] #Apply conversion to obtain uS
    return(rawEDASignal)

def emgconverter(rawEMGSignal,VCC=3.3,nBits=10):
    """
        Input: BITalino raw data in collected using Python API
                VCC in Volt, default 3.3
                nBits, number of bits, can be 10 or 6
        Output: EMG raw signal in mV
        
    NOTE: output should be in range -1.64mV - 1.64mV
    """
    #http://bitalino.com/datasheets/REVOLUTION_EMG_Sensor_Datasheet.pdf
    gain = 1009 #Sensor Gain
    rawEMGSignal = [((((ADC / 2**nBits) - (1 / 2)) * VCC ) / gEMG) for ADC in rawEMGSignal] #Apply conversio
    rawEMGSignal = [value*1000 for value in rawEMGSignal] #conversion from V to mV
    return(rawEMGSignal)
    
###############################################################################
#                                                                             #
#                                  MAIN                                       #
#                                                                             #
###############################################################################
""" 
This sections handles our MAIN process
"""
        
if(__name__ == "__main__"):
    dataset = []
    with open(basepath + "/bitalino.txt","r") as f:
        dataset = [x for x in csv.reader(f)]
    dataset = np.array(dataset[1:])
    rawEMGSignal = [float(x) for x in dataset[:,-6]]
    rawEMGSignal = emgconverter(rawEMGSignal)
    plt.plot(rawEMGSignal,color='green')
    plt.axhline(0)
    with open(basepath + '/convertedEMG.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
        pickle.dump(rawEMGSignal, f)
#    rawEDASignal = [float(x) for x in dataset[:,-4]]
#    plt.plot(rawEDASignal,color='red')
#    rawEDASignal = edaconverter(rawEDASignal)
#    plt.plot(rawEDASignal,color='green')
#    plt.axhline(0)
#    with open(basepath + '/convertedEDA.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
#        pickle.dump(rawEDASignal, f)
