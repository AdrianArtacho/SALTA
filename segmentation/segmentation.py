import numpy as np
import pandas as pd
import os


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
    if name.startswith('x'):
        return (x - zero[0]) / scale
    elif name.startswith('y'):
        return (x - zero[1]) / scale
    elif name.startswith('z'):
        return (x - zero[2]) / scale
    else:
        return x

def rescaleArray(x):
    noseIndex = index_from_landmark['left_eye_outer']
    leftEyeIndex = index_from_landmark['left_eye_outer']
    rightEyeIndex = index_from_landmark['right_eye_outer']
    nose = np.array([coord for i, coord in enumerate(x) if (i < (3*(noseIndex + 1)) and i>=(3*noseIndex))])
    leftEye = np.array([coord for i, coord in enumerate(x) if (i < (3*(leftEyeIndex + 1)) and i>=(3*leftEyeIndex))])
    rightEye = np.array([coord for i, coord in enumerate(x) if (i < (3*(rightEyeIndex + 1)) and i>=(3*rightEyeIndex))])
    scale = np.linalg.norm(leftEye - rightEye)
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