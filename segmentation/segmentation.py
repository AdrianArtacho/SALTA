import numpy as np
import pandas as pd
import os
import re
from parseannotations import parseannotations2 as pa
from utils import retrieveVideo as rV


landmarks = [
        'nose',
        'left_eye_inner', 'left_eye', 'left_eye_outer',
        'right_eye_inner', 'right_eye', 'right_eye_outer',
        'left_ear', 'right_ear',
        'mouth_left', 'mouth_right',
        'left_shoulder', 'right_shoulder',
        'left_elbow', 'right_elbow',
        'left_wrist', 'right_wrist',
        'left_pinky_1', 'right_pinky_1',
        'left_index_1', 'right_index_1',
        'left_thumb_2', 'right_thumb_2',
        'left_hip', 'right_hip',
        'left_knee', 'right_knee',
        'left_ankle', 'right_ankle',
        'left_heel', 'right_heel',
        'left_foot_index', 'right_foot_index',
    ]


index_from_landmark = {name: i for i,name in enumerate(landmarks)}


def rescaleEntry(name, x, zero, scale):
    """
    name is the name of the column where the coordinate was extrated from (X0_rescaled, etc.)
    x is a coordinate (either x, y, z), 
    zero is the 3-dimensional point at the center (could be any ppoint, such as the nose)
    scale is a normalising factor
    """
    if name.startswith('x'):
        return (x - zero[0]) / scale
    elif name.startswith('y'):
        return (x - zero[1]) / scale
    elif name.startswith('z'):
        return (x - zero[2]) / scale
    else:
        return x

def rescaleArray(x):
    """
    x is one entire data array of landmark coordinates (3 values per landmark) for a snapshot
    """
    noseIndex = index_from_landmark['left_eye_outer']
    leftEyeIndex = index_from_landmark['left_eye_outer']
    rightEyeIndex = index_from_landmark['right_eye_outer']
    
    # nose is an array with the coordinates of the landmark "nose"
    nose = np.array([coord for i, coord in enumerate(x) if (i < (3*(noseIndex + 1)) and i>=(3*noseIndex))])
    
    # leftEye is an array with the coordinates of the landmark "leftEye"
    leftEye = np.array([coord for i, coord in enumerate(x) if (i < (3*(leftEyeIndex + 1)) and i>=(3*leftEyeIndex))])
    
    # rightEye is an array with the coordinates of the landmark "rightEye"
    rightEye = np.array([coord for i, coord in enumerate(x) if (i < (3*(rightEyeIndex + 1)) and i>=(3*rightEyeIndex))])
    
    # distance between left and right eyes
    scale = np.linalg.norm(leftEye - rightEye)
    
    # This creates an array using the rescaled values
    return np.array([rescaleEntry(landmarks[int(i/3)], coord, nose, scale)
        for i, coord 
        in enumerate(x)
        if (i >= (3*(noseIndex + 1)) or i<(3*noseIndex))])


def rescale(x):
    ## nose is 0
    nose = np.array([coord for name, coord in x.items() if name[1:] == str(index_from_landmark['nose'])])
    leftEye = np.array([coord for name, coord in x.items() if name[1:] == str(index_from_landmark['left_eye_outer'])])
    rightEye = np.array([coord for name, coord in x.items() if name[1:] == str(index_from_landmark['right_eye_outer'])])
    scale = np.linalg.norm(leftEye - rightEye)
    return {(name + "_rescaled" if name[0] in ['x', 'y', 'z'] else name) : rescaleEntry(name, coord, nose, scale) for name, coord in x.items()}


def lightenUp(x, byFactor=2):
    return np.add(x, np.divide((255 - x), byFactor)).astype(int)

def kdenLiveTimeToFrame(time, fps=15):
    secs = time.split(":")
    return int(secs[0]) * 60 + int(secs[1]) * fps + int(secs[2])
    

def rescaleDf(df):
    df_rescaled_list = list()
    for i, row in df.iterrows():
        df_rescaled_list.append(rescale(row))
    return pd.DataFrame(df_rescaled_list).drop(["x0_rescaled", "y0_rescaled", "z0_rescaled"], axis=1)


def filterDf(df, mch_output):

    # return dataframe only relevant columns:
    badIndices = [i for i, lm in enumerate(landmarks) if lm not in mch_output]
    # print('baddies', badIndices)
    containsNumber = re.compile('[0-9]+')
    badColumns = []
    for col in df.columns:
        numbers = containsNumber.findall(col)
        # print(numbers)
        if len(numbers)>0:
            if int(numbers[0]) in badIndices:
                badColumns.append(col)
    # print(badColumns)
    return df.drop(badColumns, axis=1, inplace=False)


def generateTrainingDataFromPieceMaker(df, annotations, batch_size):
    """cleans and prepares data for training

    Args:
        df (pandas dataframe): input data
        annotations (dict): keys are the annotations and values are dictionaries with the following content (keys): "name", "by", "from", "till".
        batch_size (int): number of frames for training

    Returns:
        np.array: training data
    """

    trainingData = list()
    for a in annotations.values():
        ## a is one particular annotation (dict)

        subDf = df[(df.time >= a["from"]) & (df.time<=a["till"])]
        ## only data entries, no time
        subDf_temp = subDf.drop(["time"], axis=1, inplace=False)

        for wnd in subDf_temp.rolling(batch_size):
            ## iterates over all the rolling windows (wnd)
            # flattens the data
            data = wnd.values.flatten()
            print('data', data)
            print('length of data', len(data), '\n3batchsize', 3*batch_size)
            if len(data) != (subDf_temp.shape[1] * batch_size):
                continue
            trainingData.append(data)
    ret = np.array(trainingData)
    # print('ret', ret)
    return ret


def generateDataFromAnnotation(df, anno, batch_size=4, timeToFrame=kdenLiveTimeToFrame, asDict=True):
    # print('Batch size inside the annotations', batch_size)
    result = dict()
    onlyCoordinateColumns = [c for c in df.columns if c[0] in ['x', 'y', 'z']]
    for name, speclist in anno.items():
        # print(name)
        result_list = list()
        for specs in speclist:
            fr = timeToFrame(specs["from"])
            to = timeToFrame(specs["till"])
            till = to - batch_size + 1
            if till < fr:
                continue
            for i in range(fr, till + 1):
                # print('out of curiosity, whats the length of this', len(list(range((fr + i),(fr + i + batch_size)))))
                indices = range((fr + i),(fr + i + batch_size))
                dat = df.loc[indices, onlyCoordinateColumns]
                # print('size of dataframe', dat.shape)
                # print('length of data entry', len(dat.to_numpy().flatten()))
                result_list.append(dat.to_numpy().flatten())
        # print('length of the result list', len(result_list))
        result[name] = np.array(result_list)

    if asDict:
        return result
    return np.vstack(tuple(result.values()))


def loadData(fileName = "MariaMovementSequence_xyz_27Sept", fps=15, fromRoot=True):
    filename = ''
    if fromRoot:
        filename = os.path.join("data", "csv", fileName + ".csv")
    else:
        filename = os.path.join("..","data", "csv", fileName + ".csv")
        
    df = pd.read_csv(
        filename, 
        header=0,
        index_col=0)
    df["time"] = 1000 * df.index / fps
    return df

def turnDictDataIntoArray(dictData):
    return np.vstack(tuple(dictData.values()))