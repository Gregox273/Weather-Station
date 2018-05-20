#!/usr/bin/env python3

import sys
import struct
import datetime

# Useage
if len(sys.argv) != 2:
    print("Usage: {} <logfile.bin>".format(sys.argv[0]))
    sys.exit(1)

# Data Log IDs
ID_TEMP = int("0x01", 0)
ID_UV = int("0x02", 0) 
ID_LIGHT = int("0x04", 0)
ID_LOW_LIGHT = int("0x8", 0)
ID_V_LOW_LIGHT = int("0x10", 0)
ID_WIND = int("0x20", 0)
ID_VCC = int("0x40", 0)

# Event Log IDs
RTC_ERROR = int("0x80", 0)
RTC_UPDATE = int("0x81", 0)
IDLE_UPDATE = int("0x82", 0)
PAYLOAD_ERROR = int("0x83", 0)
UNKNOWN_COMMAND = int("0x84", 0)
TX_ENABLE = int("0x85", 0)
TX_DISABLE = int("0x86", 0)
SD_DUMP = int("0x87", 0)

# Nominal Supply Voltage
v_supply = 5.0
        
# Open log file
with open(sys.argv[1], 'rb') as log:

    # Read File
    log.read();

    # File pointer
    i = 0
    num_bytes = log.tell()
    
    # Loop until EOF
    while i in range(num_bytes):
        
        # Seek to next log
        log.seek(i)
        
        # Read Metadata
        header = log.read(5)    
        
        # Get Message Metadata
        meta_data = struct.unpack('<IB', header)
        time_stamp = datetime.datetime.fromtimestamp(meta_data[0]).strftime('%Y-%m-%d %H:%M:%S')
        log_type = meta_data[1]
        
        # Data - Temp
        if(log_type == ID_TEMP):
        
            payload = log.read(2)
            res = struct.unpack('<H', payload)
            temp = ((res[0]*v_supply)/(1024*5.0164))*100 - 50
            print(time_stamp, "Temp = %.2f" %temp, "C")
            i += 7 
            
        # Data - UV
        if(log_type == ID_UV):
        
            payload = log.read(2)
            res = struct.unpack('<H', payload)
            print(time_stamp, "UV =", res[0])
            i += 7 
            
        # Data - Light
        if(log_type == ID_LIGHT):
        
            payload = log.read(2)
            res = struct.unpack('<H', payload)
            print(time_stamp, "Light =", res[0])
            i += 7 
            
        # Data - Low Light
        if(log_type == ID_LOW_LIGHT):
        
            payload = log.read(2)
            res = struct.unpack('<H', payload)
            print(time_stamp, "Low Light =", res[0])
            i += 7 
            
        # Data - Very Low Light
        if(log_type == ID_V_LOW_LIGHT):
        
            payload = log.read(2)
            res = struct.unpack('<H', payload)
            print(time_stamp, "Night Light =", res[0])
            i += 7 
            
        # Data - Wind
        if(log_type == ID_WIND):
        
            payload = log.read(2)
            res = struct.unpack('<H', payload)
            print(time_stamp, "Wind =", res[0])
            i += 7    
            
        # Data - Supply Voltage
        if(log_type == ID_VCC):
        
            payload = log.read(2)
            res = struct.unpack('<H', payload)
            v_supply = res[0]/1000
            print(time_stamp, "Supply =", v_supply, "V")
            i += 7           
              
        # Event - RTC_ERROR
        if(log_type == RTC_ERROR):
        
            print(time_stamp, "EVENT - RTC ERROR")
            i += 5 
        
        # Event - RTC_UPDATE
        if(log_type == RTC_UPDATE):
        
            print(time_stamp, "EVENT - RTC_UPDATE")
            i += 5 
            
        # Event - IDLE_UPDATE
        if(log_type == IDLE_UPDATE):
        
            print(time_stamp, "EVENT - IDLE_UPDATE")
            i += 5 
            
        # Event - PAYLOAD_ERROR
        if(log_type == PAYLOAD_ERROR):
        
            print(time_stamp, "EVENT - PAYLOAD_ERROR")
            i += 5 
            
        # Event - UNKNOWN_COMMAND
        if(log_type == UNKNOWN_COMMAND):
        
            print(time_stamp, "EVENT - UNKNOWN_COMMAND")
            i += 5 
            
        # Event - TX_ENABLE
        if(log_type == TX_ENABLE):
        
            print(time_stamp, "EVENT - TX_ENABLE")
            i += 5 
            
        # Event - TX_DISABLE
        if(log_type == TX_DISABLE):
        
            print(time_stamp, "EVENT - TX_DISABLE")
            i += 5 
            
        # Event - SD_DUMP
        if(log_type == SD_DUMP):
        
            print(time_stamp, "EVENT - SD_DUMP")
            i += 5     
