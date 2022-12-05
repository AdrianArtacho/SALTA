## Load libaries

from segmentation.trainModel import Model
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


    def __init__(self) -> None:
        self.pickle = ""
        

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
    
        # run cv2 from the video to retrieve landmarks
        if fromRoot:
            lm_path = os.path.join("data", "csv", landmarkFileName + ".csv")
            lm_path_filtered = os.path.join("data", "csv", landmarkFileName + "_filtered_" + "_".join(mch_output) + ".csv")
        else:
            lm_path = os.path.join("..","data", "csv", landmarkFileName + ".csv")
            lm_path_filtered = os.path.join("..","data", "csv", landmarkFileName + "_filtered" + "_".join(mch_output) + ".csv")
        
    
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
        

    def generateDataFromPieceMaker(self, batch_size, rawMotionBankCSVPath, landmarkFileName, fromCache=False, fromRoot=False):
        """
        retrieves the landmarks from the motionbank annotations and generate taining data.
        """

        df_filtered, parseddict = self.getFilteredDataFrame(rawMotionBankCSVPath=rawMotionBankCSVPath, landmarkFileName=landmarkFileName, fromCache=fromCache, fromRoot=fromRoot)

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
                
                newData = {coord + str(j):lm.__getattribute__(coord)  for j, lm in enumerate(results.pose_landmarks.landmark) for coord in ["x", "y", "z"]}
                
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