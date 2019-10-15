# 获取目录文件列表
# 返回：文件名，完整路径

import os


def getRadFiles(road):
    if road == "":
        road = '.'
    fileList = []
    for parent, dirnames, filenames in os.walk(road, followlinks=True):
        for filename in filenames:
            file_path = os.path.join(parent, filename)
            road = (filename, file_path)
            fileList.append(road)
            # print('文件名：%s' % filename)
            # print('文件完整路径：%s\n' % file_path)
        return fileList
