"""Log data to hard drive"""
import os
import sqlite3
from .packets import *

script_dir = os.path.dirname(__file__)

def run(usb_pipe, gui_pipe, gui_exit, log_dir, db_filepath):
    db = sqlite3.connect(db_filepath)
    cursor = db.cursor()
    while not gui_exit.is_set():
        # Main loop, add incoming packets to database
        if usb_pipe.poll(0.01):
            new_pkt = usb_pipe.recv()
            try:
                with db:
                    if id in Log_PCKT_LIST:
                        db.execute('''INSERT INTO log_table(timestamp, id,
                                payload_16)
                                VALUES(?,?,?)''',
                                (new_pkt.timestamp, new_pkt.id,new_pkt.payload))
                    elif id in EVENT_PCKT_LIST:
                        db.execute('''INSERT INTO log_table(timestamp, id)
                                VALUES(?,?)''',
                                (new_pkt.timestamp, new_pkt.id))
            except sqlite3.IntegrityError:
                # Record already exists
                pass
            #finally:
                #db.close()

        # Check for commands from GUI
        if gui_pipe.poll():
            from_gui = gui+pipe.recv()
            if isinstance(from_gui,DB_Request):
                    self.usb_pipe.send(new_packet_window)

    db.close()