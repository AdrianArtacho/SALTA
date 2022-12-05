import sys
from segmentation.trainModel import Training

def main():
    ## create Training instance
    tr = Training()
    ## path name of the csv motionbank file

    typeOfFunctionCall = sys.argv[1]
    rawMotionBankCSVPath = sys.argv[2]
    landmarkFileName = sys.argv[3]

    withOptionalArguments = len(sys.argv)>4
    if withOptionalArguments:
        fromCache = True if sys.argv[4]=="True" else False
        saveOutputToCSV = True if sys.argv[5]=="True" else False
        kwargs = dict(
            rawMotionBankCSVPath=rawMotionBankCSVPath,
            landmarkFileName=landmarkFileName,
            fromCache=fromCache,
            fromRoot=True,
            saveOutputToCSV=saveOutputToCSV)
    else:
        kwargs = dict(
            rawMotionBankCSVPath=rawMotionBankCSVPath,
            landmarkFileName=landmarkFileName,
            fromRoot=True)

    
    
    if typeOfFunctionCall=='training':

        print(f'We are in {typeOfFunctionCall}')
        newKwargs = dict(**kwargs,  batch_size=(sys.argv[6] if withOptionalArguments else 3))
        res = tr.generateDataFromPieceMaker(**newKwargs)
        # print(res)
        
    elif typeOfFunctionCall=='raw':
        print(f'We are in {typeOfFunctionCall}')
        df, parse_anno = tr.getFilteredDataFrame(**kwargs)
        # print(df)

    else: 
        print("You have selected the wrong function call")


if __name__ == '__main__':
    main()