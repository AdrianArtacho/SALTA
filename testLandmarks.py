from utils import mediapipe as mp
import numpy as np
from segmentation import trainModel as tM
import sys

rawMotionBankCSVPath = ''
for i in range(1, len(sys.argv)):
    if i == 1:
        rawMotionBankCSVPath = sys.argv[i]
    #elif i == 2:
    #    verbose = bool(sys.argv[i])
    #elif i == 3:
    #    annotation_author = sys.argv[i]
    else:
        print('too many arguments.')


fromRoot = True
fromCache = False
batch_size = 3
n_components = 4

landmarkCSVFileName = 'testAgainMaria2'

print('fitting model')
tM.Model.fitModelFromMotionBank(
    batch_size=batch_size,
    n_components=n_components,
    rawMotionBankCSVPath=rawMotionBankCSVPath,
    landmarkFileName=landmarkCSVFileName,
    fromCache=fromCache,
    fromRoot=fromRoot)

print('model fitted')
lR = mp.LandmarksRetrieval()
df_filtered, _ = lR.getFilteredDataFrame(rawMotionBankCSVPath, landmarkCSVFileName, fromCache=True, fromRoot=fromRoot)
print(df_filtered.shape)
for index in range(0,df_filtered.shape[0],100):

    oneslice = range(index, index + batch_size)
    df = df_filtered.drop(["time"], axis=1, inplace=False)

    checkthis = np.array([df.iloc[oneslice,:].values.flatten()])
    pred = tM.Model.gmm.predict(checkthis)
    pred_proba = tM.Model.gmm.predict_proba(checkthis)
    

    print('pred of category for time {} is:'.format(index), pred[0])
    print('pred of probs for time {} is:'.format(index), str(pred_proba))

# tM.gmm.