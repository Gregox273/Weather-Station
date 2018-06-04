"""Log data to hard drive"""
import os
import sqlite3
from .packets import *
import time

script_dir = os.path.dirname(__file__)

def into_db(new_pkt,db,cursor,commit=True):
    try:
        #with db:
            if new_pkt.id in LOG_PCKT_LIST:
                cursor.execute('''INSERT INTO log_table(timestamp, id, payload_16)\
                        VALUES(?,?,?)''',
                        (new_pkt.timestamp, new_pkt.id,new_pkt.payload))
                if commit:
                    db.commit()

            elif id in EVENT_PCKT_LIST:
                cursor.execute('''INSERT INTO log_table(timestamp, id)\
                        VALUES(?,?)''',
                        (new_pkt.timestamp, new_pkt.id))
                if commit:
                    db.commit()
    except sqlite3.IntegrityError:
        # Record already exists
        db.rollback()

    return new_pkt

def handle_sd_dump(db,cursor,usb_pipe, gui_pipe):
    print("Storing SD dump...          ", end=" ", flush=True)
    # Read the dump into a file
    tmpfile = 'tmp.bin'
    try:
        os.remove(tmpfile)  # Remove if exists
    except OSError:
        pass
    flag = False
    while not flag:
        with open(tmpfile,'ab+') as buffer:
            for i in range(1,1000):
                # Process packets in 1000 packet batches
                if usb_pipe.poll(10):
                    new_pkt = usb_pipe.recv()
                    buffer.write(new_pkt.data_struct)
                    if new_pkt.id == SD_END:
                        print("[Done!]")
                        flag = True
                        break
                else:
                    flag = True
                    print("[Timeout!]")
                    break

    print("Adding to database...       ", end=" ", flush=True)

    # Now parse the file
    with open(tmpfile,'ab+') as buffer:
        # File pointer
        i = 0
        num_bytes = buffer.tell()

        cursor.execute('BEGIN TRANSACTION')

        # Loop until EOF
        while i in range(num_bytes):

            # Seek to next log
            buffer.seek(i)

            # Read Metadata
            header = buffer.read(EVENT_PCKT_LEN)

            # Get Message Metadata
            meta_data = struct.unpack('<BI', header)
            log_type = meta_data[0]

            if(log_type == SD_END):
                i = num_bytes + 10
                break
            else:
                #time_stamp = datetime.datetime.fromtimestamp(meta_data[1]).strftime('%Y-%m-%d %H:%M:%S')
                time_stamp = meta_data[1]

            if log_type in LOG_PCKT_LIST:
                i += LOG_PCKT_LEN
                payload = buffer.read(LOG_PCKT_LEN - EVENT_PCKT_LEN)
                res = struct.unpack('<H', payload)
                message = Log_Packet(log_type,time_stamp,res[0])
                into_db(message,db,cursor,commit=False)
                #gui_pipe.send(message)
            elif log_type in EVENT_PCKT_LIST:
                i += EVENT_PCKT_LEN
                message = Event_Packet(log_type,time_stamp)
                into_db(message,db,cursor,commit=False)
                #gui_pipe.send(message)
        db.commit()
    os.remove(tmpfile)
    print("[Done!]")
    print("Running...")


def run(usb_pipe, gui_pipe, gui_exit, log_dir, db_filepath):
    db = sqlite3.connect(db_filepath, timeout=20)
    cursor = db.cursor()

    while not gui_exit.is_set():
        # Main loop, add incoming packets to database
        if usb_pipe.poll(0.01):
            new_pkt = usb_pipe.recv()
            # if new_pkt.id in EVENT_PCKT_LIST:
            #     print(EVENT_PCKT_LIST.get(new_pkt.id)[0])
            # if new_pkt.id == SD_DUMP:
            #     handle_sd_dump(db,cursor,usb_pipe)
            # else:
            #     into_db(new_pkt,db,cursor)
            into_db(new_pkt,db,cursor)
            gui_pipe.send(new_pkt)


        # Check for commands from GUI
        if gui_pipe.poll():
            from_gui = gui_pipe.recv()
            # Respond to command here
            if from_gui == BEGIN_DUMP:
                # Handle SD dump
                handle_sd_dump(db,cursor,usb_pipe, gui_pipe)

    # Wait for USB process to end, make sure pipe doesn't fill up
    cursor.execute('BEGIN TRANSACTION')

    while usb_pipe.poll(0.2):
        new_pkt = usb_pipe.recv()
        into_db(new_pkt,db,cursor,commit=False)

    db.commit()
    db.close()
