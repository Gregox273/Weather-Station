"""Gregory Brooks (gb510), Matt Coates (mc955) 2018"""

import multiprocessing

from . import usb
from . import gui_interface
from . import logging
import time
import sys

import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)

def run():
    """Initialise and run the backend.
    """
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

    print("Starting processes...")
    # Start gui/main process
    gui_process = multiprocessing.Process(target=gui_interface.run, args=(gui_usb_pipe, gui_log_pipe, gui_exit))
    gui_process.start()

    # Start logging process
    log_process = multiprocessing.Process(target=logging.run, args=(log_usb_pipe, gui_exit, "../logs"))
    log_process.start()

    # Start usb parsing process
    usb_process = multiprocessing.Process(target=usb.run, args=(usb_gui_pipe, usb_log_pipe, gui_exit))
    usb_process.start()

    print("Running...")
    gui_process.join()
    print("Exiting...")
    print("GUI process ended")
    usb_process.join()
    print("USB process ended")
    log_process.join()
    print("Logging process ended")
    time.sleep(0.2)
