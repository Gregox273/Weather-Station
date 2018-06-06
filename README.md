# Weather Station

Gregory Brooks, Matt Coates 2018

**Setup (Ubuntu)**:
(Optional) create and activate virtual environment
```
virtualenv -p python3 venv
source venv/bin/activate
```

<br>

Install python dependencies via pip3
```
pip3 install -r requirements.txt
```

**Run with run.py**
<br><br>
Optional arguments:
<br>
--port [*serial port name (default /dev/ttyACM0)*]<br>
--baud [*baudrate (default 115200)*]<br>
-d *(enables debug mode, where incoming bytes are printed to terminal and saved into a session log file)*<br>
--file [*file to read bytes from, instead of receiving over serial*]