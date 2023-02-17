import os
import PySimpleGUI as sg

cmd_arguments = ['raw', 'data/gesturetest.csv', '2022-12-16_21-38', 'False', 'True', '3']

def parse_cmd_video2csv(cmd_arguments):
    # print('parsing...')
    # print(cmd_arguments)
    # command = 'python video2csv.py raw data/gesturetest.csv 2022-12-16_21-38 False True 3'
    V2csv_command = f"python video2csv.py {cmd_arguments[0]} {cmd_arguments[1]} {cmd_arguments[2]} {cmd_arguments[3]} {cmd_arguments[4]} {cmd_arguments[5]}"
    # print('command...')
    print(V2csv_command)
    os.system(V2csv_command)

layout = [  [sg.Text('Argument #1: choose which type of function call'), 
            sg.Combo(['raw', 'training', 'gettrainingdata'], default_value='raw', s=(13,22), enable_events=True, readonly=False, k='-functionCallType-')],
            [sg.Text('Argument #2: relative path to the raw .csv file exported from Piecemaker')],
            [sg.FilesBrowse('select inputfile', target='-input-'), 
            sg.Input('data/gesturetest.csv', key='-input-', enable_events=True, s=40)],
            [sg.Text('Argument #3: name of the output .csv file with the extracted landmarks')],
            [sg.FolderBrowse('select outputfile', target='-output-'), 
            sg.Input('exampleblaa', key='-output-', enable_events=True, s=39)],
            [sg.Text('Argument #4: from Cache (Boolean)'), 
            sg.Combo(['True', 'False'], default_value='False', s=(13,22), enable_events=True, readonly=False, k='-fromCache-')],
            [sg.Text('Argument #5: SaveOutputToCSV (Boolean)'), 
            sg.Combo(['True', 'False'], default_value='True', s=(13,22), enable_events=True, readonly=False, k='-SaveOutputToCSV-')],
            [sg.Text('Argument #6: batch size (integer)'), 
            sg.Input('3', s=15, enable_events=True, readonly=False, k='-batchSize-', justification='r')],
            [sg.OK(), sg.Button('Cancel')] ]


# **arg #6** `3` Batch size. It is an integer that defines the amount of....


window = sg.Window('video2csv', layout)

while True:
    event, values = window.read()
    #sg.popup(event, values)                     # show the results of the read in a popup Window
    # print(event, values)
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    elif event == '-functionCallType-':
        cmd_arguments[0] = values['-functionCallType-']
        # print(cmd_arguments)
    elif event == '-input-':
        cmd_arguments[1] = values['-input-']
    elif event == '-output-':
        cmd_arguments[2] = values['-output-']
    elif event == '-fromCache-':
        cmd_arguments[3] = values['-fromCache-']
    elif event == '-SaveOutputToCSV-':
        cmd_arguments[4] = values['-SaveOutputToCSV-']
    elif event == '-batchSize-':
        cmd_arguments[5] = values['-batchSize-']
    elif event == 'OK':
        # print(cmd_arguments)
        #window.close()
        parse_cmd_video2csv(cmd_arguments)
        window.close()

window.close()


