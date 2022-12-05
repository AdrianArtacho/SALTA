from sklearn.mixture import GaussianMixture
import scipy
import numpy as np
import segmentation.segmentation as sg 
import utils.mediapipe as mp

Annotations = {
    "hip_joint_right": [
        {"from": "00:05:12", "till": "00:07:11"},
        {"from": "00:44:03", "till": "00:46:03"}],
    "elbow_hinge_left": [
        {"from": "00:07:14", "till":"00:11:07"},
        {"from": "00:46:03", "till":"00:48:06"}],
    "pivot_right":[{"from": "00:48:07", "till": "00:49:13"}],
    "pivot_left":[{"from": "00:50:04", "till": "00:52:03"}],
    "rotation_shoulder_left": [{"from": "00:11:08" , "till":"00:14:02"}],
    "thumb_movement_left": [{"from": "00:14:03", "till": "00:18:10"}],
    "knee_hinge_right":[{"from":"00:18:11", "till": "00:21:01"}]
}

class Model:
    
    gmm : GaussianMixture

    # def __init__(self):
    #     self.gmm = None

    def setGMM(fileName, anno=Annotations, fps=15, batch_size=3, timeToFrame=sg.kdenLiveTimeToFrame, asDict=False):
        ## Load dataframe from file
        df = sg.loadData(fileName=fileName, fps=fps)
        print('--> Dataframe has been loaded into df object.')
        ## rescale entries
        df_rescaled = sg.rescaleDf(df)
        print('--> Landmarks have been recentered around the nose and rescaled by the distance between the eyes.')
        # ## get datapoints from annotations
        print('batch size before generating result', batch_size)
        result = sg.generateDataFromAnnotation(
            df=df_rescaled,
            anno=anno,
            batch_size=batch_size, 
            timeToFrame=timeToFrame,
            asDict=asDict)
        
        print('--> Start training.')
        print('dimensions of result: ', result.shape )
        Model.gmm = GaussianMixture(n_components=len(Annotations.keys()), random_state=0).fit(result)


    def fitModelFromMotionBank(batch_size, n_components, rawMotionBankCSVPath, landmarkFileName, fromCache=False, fromRoot=False):
        """
        This function first generates darta (landmarks) from the motion bank video
        and then fits the GMM model with that data.
        """
        # for rawMotionBankCSVPath in rawMotionBankCSVPaths:
        lR = mp.LandmarksRetrieval()
        result = lR.generateDataFromPieceMaker(batch_size=batch_size, rawMotionBankCSVPath=rawMotionBankCSVPath, landmarkFileName=landmarkFileName, fromCache=fromCache, fromRoot=fromRoot)
        Model.gmm = GaussianMixture(n_components=n_components, random_state=0).fit(result)
