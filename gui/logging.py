"""Log data to hard drive"""
import os

script_dir = os.path.dirname(__file__)

def run(usb_pipe, gui_exit, log_dir):
    os.makedirs(os.path.abspath(os.path.join(script_dir,log_dir)), exist_ok=True)
    txt_log_filepath = os.path.abspath(os.path.join(script_dir,log_dir,"txt_log.txt"))
    json_log_filepath = os.path.abspath(os.path.join(script_dir,log_dir,"json_log.txt"))
    with open(txt_log_filepath, 'a+') as f_txt, open(json_log_filepath, 'a+') as f_json:
        while not gui_exit.is_set():
            ## Main loop
            if usb_pipe.poll(0.01):
                new_packet = trilat_pipe.recv()
                new_packet.print_to_file(f_txt)
                new_packet.print_to_js(f_json)
    f_txt.closed
    f_json.closed