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

def Keithley6517Measure(func='v', rang=0, N=10, nplc=5, guard=False, address='ASRL5::INSTR'):
    

    delayCom=0.3

    GUARD = 'ON' if guard else 'OFF'

    if func in ['V', 'v']:
        FUNC = 'VOLT'
        guard = True
        minRange = '2'
    elif func in ['I', 'i']:
        FUNC = 'CURR'
        minRange = '20e-12'
    elif func in ['R', 'r']:
        FUNC = 'RES'
        guard = True
    elif func in ['Q', 'q']:
        FUNC = 'CHAR'
        minRange = '2e-9'
    else:
        FUNC = func

    if rang in [0,'0','auto','AUTO']:
        RANG = ':AUTO ON'
    elif isinstance(rang, (int, float)):
        RANG = f' {rang:e}'
    else:
        RANG = ' ' + rang
        

    rm = pyvisa.ResourceManager()
    g1 = rm.open_resource(address)
    
    try:
        info=g1.query('*IDN?')
    except:
        try:
            g1.read_termination = '\r'
            g1.write_termination = '\r'
            g1.baud_rate = 9600
            info=g1.query('*IDN?')
        except:
            info="Connection unsuccessful!"
            print(info)
            return
    
    
    g1.timeout = 10000*N

    g1.write('*RST')
    time.sleep(delayCom)
    g1.write('SYST:ZCH ON')
    if guard:
        time.sleep(delayCom)
        g1.write(f'{FUNC}:GUAR {GUARD}')

    time.sleep(delayCom)
    g1.write(f"FUNC '{FUNC}'")

    time.sleep(delayCom)
    g1.write(f'{FUNC}:RANG {minRange}')

    time.sleep(delayCom)
    g1.write('SYST:ZCOR ON')
    time.sleep(1)
    g1.write(f'{FUNC}:RANG{RANG}')
    time.sleep(delayCom)
    g1.write('SYST:ZCH OFF')
    if FUNC != 'RES':
        time.sleep(delayCom)
        g1.write(f'{FUNC}:NPLC {nplc}')

    time.sleep(delayCom)
    g1.write('trac:cle')
    time.sleep(delayCom)
    g1.write(f'trig:coun {N}')
    time.sleep(delayCom)
    g1.write(f'trac:poin {N}')
    time.sleep(delayCom)
    g1.write('form:elem read,tst')
    time.sleep(delayCom)
    g1.write('trac:feed:cont NEXT')
    time.sleep(delayCom)
    g1.write(':init; *wai')
    time.sleep(delayCom)
    received = g1.query('trac:data?')


    data = np.zeros((N*2,))
    data[:] = np.fromstring(received, sep=',')

    out = np.zeros((N,2))
    out[:,1]=data[::2]
    out[:,0]=data[1::2]-data[1]

    g1.close()
    del g1

    return out

args=sys.argv[1:]
defaults=["v",0,10,5,False,'ASRL5::INSTR']

for i,arg in enumerate(args):
    defaults[i] = arg
    
v=defaults[2]
if isinstance(v, str):
    defaults[2]=int(defaults[2])

v=defaults[4]
if isinstance(v, str):
    defaults[4]=v.lower() in ("yes", "true", "t", "1")

out=Keithley6517Measure(*defaults)
        