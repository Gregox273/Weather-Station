#!/bin/bash
# Build TOAD gui from QT4 Designer ui files
# Gregory Brooks(gb510), Matt Coates(mc955) 2018

parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")"  ; pwd -P )
cd "$parent_path"

# Build subframes

# Build main window
pyuic4 -w ui/main_window.ui -o main_window.py

###OLD STUFF BELOW HERE###
# # Create basic toad_frame class
# pyuic4 -w ui/toad_frame.ui -o toad_frame.py
#
# # Create frames for each toad unit
# pyuic4 -w ui/toad_frame_master.ui -o toad_frame_master.py
# pyuic4 -w ui/toad_frame_1.ui -o toad_frame_1.py
# pyuic4 -w ui/toad_frame_2.ui -o toad_frame_2.py
# pyuic4 -w ui/toad_frame_3.ui -o toad_frame_3.py
# pyuic4 -w ui/toad_frame_4.ui -o toad_frame_4.py
# pyuic4 -w ui/toad_frame_5.ui -o toad_frame_5.py
# pyuic4 -w ui/toad_frame_6.ui -o toad_frame_6.py
#
# # Build main window
#
#
# pyuic4 ui/toad_gui.ui -o toad_gui.py