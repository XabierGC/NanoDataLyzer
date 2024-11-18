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

import pyvisa as visa # http://github.com/hgrecco/pyvisa


rm = visa.ResourceManager()

address=rm.list_resources()
info=list(address)

for i in range(0,len(address)):
    print(address[i])
    
    try:
        my_instrument = rm.open_resource(address[i])
        info[i]=my_instrument.query('*IDN?')
    except:
        try:
            my_instrument.read_termination = '\r'
            my_instrument.write_termination = '\r'
            my_instrument.baud_rate = 9600
            info[i]=my_instrument.query('*IDN?')
        except:
            info[i]=""
    print(info[i])
    my_instrument.close()
rm.close()