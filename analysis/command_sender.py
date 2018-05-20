import serial

a = [int("0xAA", 0), int("0x88", 0), int("0x10", 0), int("0x00", 0), int("0x00", 0), int("0x00", 0)]
b = bytearray(a)
with serial.Serial('/dev/ttyACM0', 115200) as ser:
    ser.write(b)
    ser.write(b)
    ser.write(b)
