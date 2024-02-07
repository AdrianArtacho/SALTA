## Load libaries
from sklearn.mixture import GaussianMixture
import scipy
import numpy as np # Adrian added this, seemed to be missing

import os 
import pandas as pd
import mediapipe as mp
import pickle

import cv2
from parseannotations import parseannotations2 as pa
from parseannotations import landmarks_mp
from utils import retrieveVideo as rV
import segmentation.segmentation as sg

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose


"""
Extract and train GMM
"""


## Gets data from piecemaker and youtube, 
## extracts landmarks
## It updates the model
# 
# 

def createFileName(output_channels):
    output_channels.sort(reverse=False)
    hashed_file_name = ""
    stringified_output = "_".join(output_channels)
    if len(stringified_output)>50:
        hashed_file_name = stringified_output[0:29] + "__" + str(abs(hash(stringified_output[29:])))
    else:
        hashed_file_name = stringified_output
    return hashed_file_name

 
def getFrameRate(video, verbose=False):
  (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
  # With webcam get(CV_CAP_PROP_FPS) does not work.
  # Let's see for ourselves.

  if int(major_ver)  < 3 :
      fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
      if verbose:
        print("Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps))
  else :
      fps = video.get(cv2.CAP_PROP_FPS)
      if verbose:
        print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))
  
  return fps


class Training:


    def __init__(self, picklepath = "somewhere.pickle") -> None:
        self.pickle = os.path.join(os.getcwd(), picklepath)
        self.gmm = None

    def loadGMM(self):
        self.gmm = pickle.load(open(self.pickle, "rb"))
        

    def retrieveData(self, filepath):
        """retrieves data from Piecemaker through csv-file
        """
    

    def getFilteredDataFrame(self, rawMotionBankCSVPath, landmarkFileName, fromCache=False, fromRoot=False, saveOutputToCSV=True):
        """
        Retrieves the youtube link from the rawMotionBankCSVPath and extracts the landmarks
        """
        # retrieve URL of youtube video and annotation dict from raw motion bank path
        url, parseddict = pa.parseCSV(rawMotionBankCSVPath)
        # convert url into cv2 readable input
        videoURL = rV.retrieveVideo(url=url)


        # run the landmark multiple choice filter
        mch_output =  landmarks_mp.chooselandmarks()
        
        hashed_file_name = createFileName(mch_output)

        # run cv2 from the video to retrieve landmarks
        landmarkFileName = (landmarkFileName[:-4] if landmarkFileName.endswith('.csv') else landmarkFileName)
        if fromRoot:

            lm_path = os.path.join(os.getcwd(), "data", "csv", landmarkFileName + ".csv")
            lm_path_filtered = os.path.join(os.getcwd(), "data", "csv", landmarkFileName + "_filtered_" + hashed_file_name + ".csv")
        else:

            lm_path = os.path.join(os.getcwd(), "..","data", "csv", landmarkFileName + ".csv")
            lm_path_filtered = os.path.join(os.getcwd(), "..","data", "csv", landmarkFileName + "_filtered" + hashed_file_name + ".csv")
        
    
        if fromCache:
            df = pd.read_csv(lm_path, header=0, index_col=0)
        else:
            df = self.createLandmarks(videoURL, landmarkFileName, fromWebCam=False, fromRoot=fromRoot)

        
        # rescale df
        df_rescaled = sg.rescaleDf(df)
        # select relevant columns in df
        df_filtered = sg.filterDf(df=df_rescaled, mch_output=mch_output)

        if saveOutputToCSV:
           df_filtered.to_csv(lm_path_filtered)
    
        return df_filtered, parseddict
  

    def generateDataFromPieceMaker(self, batch_size, rawMotionBankCSVPath, landmarkFileName, fromCache=False, fromRoot=False, saveOutputToCSV=True):
        """
        retrieves the landmarks from the motionbank annotations and generate taining data.
        """

        df_filtered, parseddict = self.getFilteredDataFrame(rawMotionBankCSVPath=rawMotionBankCSVPath, landmarkFileName=landmarkFileName, fromCache=fromCache, fromRoot=fromRoot,saveOutputToCSV=saveOutputToCSV)

        # get the training data
        result = sg.generateTrainingDataFromPieceMaker(
                df=df_filtered,
                annotations=parseddict,
                batch_size=batch_size)

        # show data
        return result



    def createLandmarks(self, url, landmarkFileName, fromWebCam=False, fromRoot=False):
        
        PoseData = []
        cap = cv2.VideoCapture(url)
        # cap = cv2.VideoCapture(os.path.join('..', datadirectory, 'MariaDancingSequenceAnotherOne.webm'))
        i = 0
        # MaxRecordings = 10
        pose = mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5)  # as pose:

        fps = getFrameRate(video=cap)
        oldTime = 0
        while cap.isOpened():
        
            i += 1
            
            success, image = cap.read()
            if not success:
                print("Ignoring empty frame.")
                # If loading a video, use 'break' instead of 'continue'.
                break

            try: # findPose:
            # Draw the pose annotation on the image.
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                height, width = image.shape[:2]
                image = cv2.resize(image, dsize=(2*width, 2*height), interpolation=cv2.INTER_CUBIC)
                results = pose.process(image)
                mp_drawing.draw_landmarks(
                    image,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
                
                #----------------OLD, buggy
                newData = {coord + str(j):lm.__getattribute__(coord)  for j, lm in enumerate(results.pose_landmarks.landmark) for coord in ["x", "y", "z"]}
                #----------------NEW, fixed?
                if results.pose_landmarks:
                    newData = {coord + str(j):lm.__getattribute__(coord) for j, lm in enumerate(results.pose_landmarks.landmark) for coord in ["x", "y", "z"]}
                else:
                    print("NO LANDMARKS DETECTED!")
                    # If results.pose_landmarks is None, handle the situation, for example, by creating an empty newData or logging the lack of detection.
                    # This block is where you should handle cases where no landmarks are detected.
                    # For example, you can create an empty dictionary with np.nan values or log the frame with no detections.
                    # newData = {coord + str(j):np.nan for j in range(expected_number_of_landmarks) for coord in ["x", "y", "z"]}
                    # newData.update({'time': oldTime})
                    # PoseData.append(newData)
                #--------------------------

                newData.update({'time': oldTime})
                PoseData.append(newData)
            
            except Exception as ex:
                newData = {coord + str(j):np.nan  for j, lm in enumerate(results.pose_landmarks.landmark) for coord in ["x", "y", "z"]}
                newData.update({'time': oldTime})
                PoseData.append(newData)

                print('didnt work', ex)
                # print(ex)
            # update time
            oldTime += 1/fps

            # Flip the image horizontally for a selfie-view display.
            if fromWebCam:
                image = cv2.flip(image, 1)
            cv2.imshow('MediaPipe Pose', image)
            if (cv2.waitKey(5) & 0xFF == 27): ## or i>MaxRecording s :
                break
        cap.release()
        df = pd.DataFrame(PoseData)

        if fromRoot:
            filename = os.path.join("data", "csv", landmarkFileName + ".csv")
        else:
            filename = os.path.join("..","data", "csv", landmarkFileName + ".csv")
            
        # df['fps'] = fps
        df.to_csv(filename)
        cv2.destroyAllWindows()
        return df

    def fitModel(self, n_components, data):
        self.gmm = GaussianMixture(n_components=n_components, random_state=0).fit(data)


    def pickleModel(self):
        pickle.dump(self.gmm, open(self.pickle, "wb"))


class Model:
    
    gmm : GaussianMixture

    # def __init__(self):
    #     self.gmm = None

    def setGMM(fileName, anno, fps=15, batch_size=3, timeToFrame=sg.kdenLiveTimeToFrame, asDict=False):
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
        # for rawMotionBankCSVPath in rawMotionBankCSVPaths:
        lR = mp.LandmarksRetrieval()
        result = lR.generateDataFromPieceMaker(batch_size=batch_size, rawMotionBankCSVPath=rawMotionBankCSVPath, landmarkFileName=landmarkFileName, fromCache=fromCache, fromRoot=fromRoot)
        Model.gmm = GaussianMixture(n_components=n_components, random_state=0).fit(result)
