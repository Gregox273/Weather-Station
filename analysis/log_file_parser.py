#!/usr/bin/env python3

import sys
import struct
import datetime
import matplotlib.pyplot as plt

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
SD_WIPE = int("0x88", 0)
SD_END = int("0x90", 0)

# Nominal Supply Voltage
v_supply = 5.0

# Amplifier Gains
temp_gain = 5.0164
uv_gain = 5.0142
v_low_light_gain = 33.9525

# Resistor Values
light_res = 995.823
low_light_res = 32876.6

plot_list = []
plt_stamp = []


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
        meta_data = struct.unpack('<BI', header)
        log_type = meta_data[0]

        if(log_type == SD_END):
            i = num_bytes + 10
            break
        else:
            time_stamp = datetime.datetime.fromtimestamp(meta_data[1]).strftime('%Y-%m-%d %H:%M:%S')
            plt_time_stamp = meta_data[1]
            
        # Data - Temp
        if(log_type == ID_TEMP):

            payload = log.read(2)
            res = struct.unpack('<H', payload)
            temp = ((res[0]*v_supply)/(1024*temp_gain))*100 - 50
            print(time_stamp, "Temp = %.2f" %temp, "C")
            plot_list.append(temp)
            plt_stamp.append(plt_time_stamp)
            i += 7

        # Data - UV
        if(log_type == ID_UV):

            payload = log.read(2)
            res = struct.unpack('<H', payload)
            vout = ((res[0]*v_supply)/(1024*uv_gain))
            uv = vout/(4.3*0.026)
            power = vout/(4.3*0.113)
            print(time_stamp, "UV-A Power = %.3f" %power, "mW/cm^2")
            print(time_stamp, "UV Index = %.2f" %uv)
            i += 7

        # Data - Light
        if(log_type == ID_LIGHT):

            payload = log.read(2)
            res = struct.unpack('<H', payload)
            vout = (res[0]/1024)*v_supply
            i_ph = vout/light_res
            i_ph_ma = i_ph*1000
            print(time_stamp, "Light = %.3f" %i_ph_ma, "mA")
            i += 7

        # Data - Low Light
        if(log_type == ID_LOW_LIGHT):

            payload = log.read(2)
            res = struct.unpack('<H', payload)
            vout = (res[0]/1024)*v_supply
            i_ph = vout/low_light_res
            i_ph_ua = i_ph*1000000
            print(time_stamp, "Low Light = %.3f" %i_ph_ua, "uA")
            i += 7

        # Data - Very Low Light
        if(log_type == ID_V_LOW_LIGHT):

            payload = log.read(2)
            res = struct.unpack('<H', payload)
            vout = ((res[0]*v_supply)/(1024*v_low_light_gain))
            i_ph = vout/low_light_res
            i_ph_ua = i_ph*1000000
            print(time_stamp, "Night Light = %.3f" %i_ph_ua, "uA")
            i += 7

        # Data - Wind
        if(log_type == ID_WIND):

            payload = log.read(2)
            res = struct.unpack('<H', payload)
            freq = res[0]/3.0
            print(time_stamp, "Wind = %.2f" %freq, "Hz")
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

            print(" ")
            print(time_stamp, "EVENT - RTC ERROR")
            print(" ")
            i += 5

        # Event - RTC_UPDATE
        if(log_type == RTC_UPDATE):

            print(" ")
            print(time_stamp, "EVENT - RTC_UPDATE")
            print(" ")
            i += 5

        # Event - IDLE_UPDATE
        if(log_type == IDLE_UPDATE):

            print(" ")
            print(time_stamp, "EVENT - IDLE_UPDATE")
            print(" ")
            i += 5

        # Event - PAYLOAD_ERROR
        if(log_type == PAYLOAD_ERROR):

            print(" ")
            print(time_stamp, "EVENT - PAYLOAD_ERROR")
            print(" ")
            i += 5

        # Event - UNKNOWN_COMMAND
        if(log_type == UNKNOWN_COMMAND):

            print(" ")
            print(time_stamp, "EVENT - UNKNOWN_COMMAND")
            print(" ")
            i += 5

        # Event - TX_ENABLE
        if(log_type == TX_ENABLE):

            print(" ")
            print(time_stamp, "EVENT - TX_ENABLE")
            print(" ")
            i += 5

        # Event - TX_DISABLE
        if(log_type == TX_DISABLE):

            print(" ")
            print(time_stamp, "EVENT - TX_DISABLE")
            print(" ")
            i += 5

        # Event - SD_DUMP
        if(log_type == SD_DUMP):

            print(" ")
            print(time_stamp, "EVENT - SD_DUMP")
            print(" ")
            i += 5

        # Event - SD_WIPE
        if(log_type == SD_WIPE):

            print(" ")
            print(time_stamp, "EVENT - SD_WIPE")
            print(" ")
            i += 5


plt.plot(plt_stamp, plot_list)
plt.show()
