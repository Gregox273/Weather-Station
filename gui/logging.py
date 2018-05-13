"""Log data to hard drive"""
import os
import sqlite3
from .packets import *

script_dir = os.path.dirname(__file__)

def run(usb_pipe, gui_exit, log_dir):
    # Set up sqlite3 database on hard drive
    try:
        os.makedirs(os.path.abspath(os.path.join(script_dir,log_dir)), exist_ok=True)
        db_filepath = os.path.abspath(os.path.join(script_dir,log_dir,"datalogger_db"))

        db = sqlite3.connect(db_filepath)
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS log_table(timestamp INTEGER NOT NULL,
                                                 id INTEGER(3) NOT NULL,
                                                 payload_16 SMALLINT,
                                                 lat DECIMAL(9,6),
                                                 lon DECIMAL(9,6),
                                                 height DECIMAL(5,3),
                                                 gps_time INTEGER,
                                                 num_sat INTEGER(3),
                                                 CONSTRAINT Packet_ID PRIMARY KEY (timestamp, id))
        ''')
        db.commit()
    except Exception as e:
        db.rollback()
        raise # -*- coding: utf-8 -*-
    finally:
        db.close()

    while not gui_exit.is_set():
        # Main loop, add incoming packets to database
        if usb_pipe.poll(0.01):
            new_pkt = usb_pipe.recv()
            try:
                with db:
                    if new_pkt.id == Identifier.GPS:
                        db.execute('''INSERT INTO log_table(timestamp, id,
                                lat, lon, height, gps_time, num_sat)
                                VALUES(?,?,?,?,?,?,?)''',
                                (new_pkt.timestamp, new_pkt.identifier,
                                new_pkt.latitude, new_pkt.longitude,
                                new_pkt.height, new_pkt.gps_time))
                    else:
                        # Generic adc reading
                        db.execute('''INSERT INTO log_table(timestamp, id,
                                payload)
                                VALUES(?,?,?)''',
                                (new_pkt.timestamp, new_pkt.identifier,
                                new_pkt.payload))
            except sqlite3.IntegrityError:
                # Record already exists
                pass
            finally:
                db.close()

        # Check for commands from GUI