"""Gregory Brooks (gb510), Matt Coates (mc955) 2018"""

import multiprocessing

from . import usb
from . import gui_interface
from . import logging
import time
import sys
import os
import sqlite3
from .packets import *
import argparse

import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)

def run():
    """Initialise and run the backend.
    """

    # Process arguments
    parser = argparse.ArgumentParser(description= \
        'Connect to weather station on given serial port (default /dev/ttyACM0)')
    parser.add_argument('--port', dest='port', type=str, nargs='?', \
        default='/dev/ttyACM0', help='Serial port to use')

    parser.add_argument('--baud', dest='baud', type=int, nargs='?', \
        default=115200, help='Baud rate')

    parser.add_argument("-d", "--debug", help="print incoming serial",
                    action="store_true")

    parser.add_argument('--file', dest='file', type=str, nargs='?', help='Log file to read')

    Args = parser.parse_args()

    ############################################################################
    # Create communication links between processes:
    ############################################################################
    print("Initialising...")

    # Pipe USB data to logging processes
    log_usb_pipe, usb_log_pipe = multiprocessing.Pipe(duplex=False)

    # Duplex pipe between usb and gui processes
    usb_gui_pipe,gui_usb_pipe = multiprocessing.Pipe(True)

    # Duplex pipe between logging and gui processes
    log_gui_pipe,gui_log_pipe = multiprocessing.Pipe(True)

    ############################################################################
    # Define and start processes
    ############################################################################
    gui_exit = multiprocessing.Event()# Flag for gui exit
    gui_exit.clear()

    # Set up sqlite3 database on hard drive
    script_dir = os.path.dirname(__file__)
    log_dir = "../logs"
    db_dir = "../logs/db"
    try:
        os.makedirs(os.path.abspath(os.path.join(script_dir,log_dir)), exist_ok=True)
        os.makedirs(os.path.abspath(os.path.join(script_dir,db_dir)), exist_ok=True)
        db_filepath = os.path.abspath(os.path.join(script_dir,db_dir,"datalogger_db"))

        db = sqlite3.connect(db_filepath,timeout=20)
        cursor = db.cursor()
        cursor.execute('PRAGMA synchronous=OFF')  # Speed up writing, database may be corrupted if computer powers off
        cursor.execute('PRAGMA journal_mode=wal')
        cursor.execute('PRAGMA Pooling=True')
        cursor.executescript("""
            DROP TABLE IF EXISTS log_table;
            CREATE TABLE log_table(
                timestamp INTEGER NOT NULL,
                id INTEGER(3) NOT NULL,
                payload_16 SMALLINT);
        """)
        db.commit()
    except Exception as e:
        db.rollback()
        raise # -*- coding: utf-8 -*-
    finally:
        db.close()

    print("Starting processes...")
    # Start gui/main process
    gui_process = multiprocessing.Process(target=gui_interface.run, args=(gui_usb_pipe, gui_log_pipe, gui_exit, db_filepath))
    gui_process.start()

    print("Running...")

    # Start logging process
    log_process = multiprocessing.Process(target=logging.run, args=(log_usb_pipe, log_gui_pipe, gui_exit, log_dir, db_filepath, Args))
    log_process.start()

    # Start usb parsing process
    usb_process = multiprocessing.Process(target=usb.run, args=(usb_gui_pipe, usb_log_pipe, gui_exit, Args))
    usb_process.start()

    usb_process.join()
    print("Exiting...")
    print("USB process ended")
    print("Finishing up logging...      ", end="")

    log_process.join()
    print("[DONE!]")
    print("Logging process ended")

    gui_process.join()
    print("GUI process ended")

    # if usb_process.is_alive():
    #     usb_process.terminate()
    #     usb_process.join()


    time.sleep(0.2)
