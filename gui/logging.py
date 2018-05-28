"""Log data to hard drive"""
import os
import sqlite3
from .packets import *

script_dir = os.path.dirname(__file__)

def run(usb_pipe, gui_pipe, gui_exit, log_dir, db_filepath):
    db = sqlite3.connect(db_filepath, timeout=20)
    cursor = db.cursor()
    while not gui_exit.is_set():
        # Main loop, add incoming packets to database
        if usb_pipe.poll(0.01):
            new_pkt = usb_pipe.recv()
            try:
                with db:
                    if new_pkt.id in LOG_PCKT_LIST:
                        cursor.execute('''INSERT INTO log_table(timestamp, id, payload_16)\
                                VALUES(?,?,?)''',
                                (new_pkt.timestamp, new_pkt.id,new_pkt.payload))
                        db.commit()

                    elif id in EVENT_PCKT_LIST:
                        cursor.execute('''INSERT INTO log_table(timestamp, id)\
                                VALUES(?,?)''',
                                (new_pkt.timestamp, new_pkt.id))
                        db.commit()
            except sqlite3.IntegrityError:
                # Record already exists
                db.rollback()
            #finally:
                #db.close()
            gui_pipe.send(new_pkt)

        # Check for commands from GUI
        if gui_pipe.poll():
            from_gui = gui_pipe.recv()
            # Respond to command here
            pass

    db.close()