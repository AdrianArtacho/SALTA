# import gui_abstractions.display_message as display_message
import gui.display_text as display_text
# import gui_abstractions.gui_popup as gui_popup
import gui.gui_button as gui_button
# import os
# import subprocess
import pyt.paths.run_subrepo_script as run_subrepo_script

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
    subrepo_dir = 'imuextract'
    scriptfile = 'IMUEXTRACT.py'
    returned = run_subrepo_script.main(subrepo_dir, scriptfile)
    print(returned)
