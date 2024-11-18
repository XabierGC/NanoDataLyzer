# -*- coding: utf-8 -*-
#%% Install before use
'''
Problems with NIvisa on Mac, preferably use PC

Must install these packages in anaconda prompt for code to run:

   conda install -c conda-forge pyvisa 
   conda install -c conda-forge pyvisa-py 
   conda install -c conda-forge pyusb 

Then install NI-VISA from:

https://www.ni.com/en-gb/support/downloads/drivers/download.ni-visa.html#442805
'''

import sys
import pyvisa # http://github.com/hgrecco/pyvisa
import time # std module
import numpy as np # http://www.numpy.org/

def Keithley263xCurrentMeasure(address, Timespan, Tstep, Tres, Irange, Ilimit, Vrange):
    rm = pyvisa.ResourceManager()
    g1 = rm.open_resource(address)

    # Definitions
    Timespan = float(Timespan)
    Tstep = float(Tstep)
    Tres = float(Tres)
    Irange = float(Irange)
    Ilimit = min(float(Ilimit), Irange)

    fgrid = 50
    Srate = Tstep * fgrid * 1
    N = int(np.floor(Timespan / Tstep))

    Vlevel = 0
    Vrange = Vrange

    # Initialization
    g1.write('smua.reset()')
    g1.write('smua.nvbuffer1.clear()')

    g1.write('format.data = format.ASCII')
    g1.write('display.screen=display.SMUA')
    g1.write('display.smua.measure.func=display.MEASURE_DCAMPS')

    g1.write('smua.measure.autorangev = smua.AUTORANGE_OFF')

    g1.write('smua.source.limiti= {}'.format(Ilimit))
    g1.write('smua.measure.rangei= {}'.format(Irange))
    g1.write('smua.source.levelv={}'.format(Vlevel))
    g1.write('smua.source.rangev={}'.format(Vrange))

    g1.write('smua.source.func=smua.OUTPUT_DCVOLTS')
    g1.write('N ={}'.format(N))
    g1.write('smua.measure.count =N')
    g1.write('smua.measure.interval = {}'.format(Tstep))
    g1.write('smua.measure.nplc = {}'.format(Srate))

    g1.write('smua.nvbuffer1.collecttimestamps = 1')
    g1.write('smua.nvbuffer1.timestampresolution = {}'.format(Tres))
    g1.write('smua.source.output = smua.OUTPUT_ON')

    g1.write('beeper.beep(0.1,2400)')
    g1.write('digio.writebit(14,1)')
    
    g1.timeout = 1000*Timespan*1.5
    n=g1.query('smua.measure.overlappedi(smua.nvbuffer1)\nwaitcomplete()\nprint(N)')
    

    g1.write('digio.writebit(14,0)')
    g1.write('smua.source.output = smua.OUTPUT_OFF')
    g1.write('beeper.beep(0.1,2400)')

    # Printing
    
    g1.timeout = 100*N
    
    received = g1.query('printbuffer(1, {}, smua.nvbuffer1.timestamps,smua.nvbuffer1) '.format(N))
    g1.write('beeper.beep(0.1,1400)')

    g1.write('smua.reset()')
    g1.write('smua.nvbuffer1.clear()')

    g1.close()
    
    data = np.zeros((N*2,))
    data[:] = np.fromstring(received, sep=',')

    out = np.zeros((N,2))
    out[:,0]=data[::2]-data[0]
    out[:,1]=data[1::2]

    

    return out


args=sys.argv[1:]
defaults=['GPIB0::26::INSTR',10,.01,.005,5,4,1e-8]

for i,arg in enumerate(args):
    defaults[i] = arg
    if i>0:
        if isinstance(arg, str):
            defaults[i]=float(defaults[i])

    
out=Keithley263xCurrentMeasure(*defaults)

