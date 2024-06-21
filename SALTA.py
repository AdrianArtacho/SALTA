# import gui_abstractions.display_message as display_message
import gui.display_text as display_text
# import gui_abstractions.gui_popup as gui_popup
import gui.gui_button as gui_button
import os
import subprocess
# import imuextract.IMUEXTRACT as IMUEXTRACT
# import imuextract.time_string as time_string

infowidth = 600
infoheight = 400
infodivisor = 25

infostep = "Step 1"
infotext = "Choose the modality of the captured data..."
display_text.main(infostep+": "+infotext, title=infostep, target_width=infowidth, target_height=infoheight, divisor=infodivisor)

options = [ 'MPIPE', 'AUDIO', 'IMU']
choice = gui_button.main(options, default_option=0, dialog_text="Select an Option", title="Choice")
print("You chose", choice)

if choice == options[2]: #IMU
    new_directory = 'imuextract'
    os.chdir(new_directory)
    # IMUEXTRACT()





# Path to the directory containing 'ímuextract' and its '.venv' folder
imuextract_dir = 'imuextract'

# Command to activate virtual environment and run the script
command = [
    'bash', '-c', 
    'source {}/.venv/bin/activate && python {}/ímuextract/IMUEXTRACT.py'.format(imuextract_dir, imuextract_dir)
]

# Execute the command
subprocess.run(command, shell=True)
