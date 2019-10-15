


import os
import routine.GetRoadFilesList as GetFileList

if __name__ == '__main__':
    fileList = os.listdir('./data/csvs_from_camera')
    for fileinfo in fileList:
        print(fileinfo)


