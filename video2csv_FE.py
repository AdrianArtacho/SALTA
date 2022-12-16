import os
import PySimpleGUI as sg

values = ['raw', 'data/gesturetest.csv', '2022-12-16_21-38', 'False', 'True', '3']

layout = [  [sg.Text('Argument #1: choose which type of function call'), 
            sg.Combo(['raw', 'training', 'gettrainingdata'], default_value='raw', s=(13,22), enable_events=True, readonly=False, k='-functionCallType-')],
            [sg.Text('Argument #2: relative path to the raw .csv file exported from Piecemaker')],
            [sg.FolderBrowse(target='-input-'), sg.Input(key='-input-')],
            [sg.Text('Argument #3: name of the output .csv file with the extracted landmarks')],
            [sg.FolderBrowse(target='-output-'), sg.Input(key='-output-')],
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
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    print('You entered ', values[0])

window.close()

# command = 'python video2csv.py raw data/gesturetest.csv 2022-12-16_21-38 False True 3'
# os.system(command)