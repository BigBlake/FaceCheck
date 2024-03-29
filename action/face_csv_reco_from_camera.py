# 摄像头实时人脸识别
# Real-time face recognition


import dlib          # 人脸处理的库 Dlib
import numpy as np   # 数据处理的库 numpy
import cv2           # 图像处理的库 OpenCv
import pandas as pd  # 数据处理的库 Pandas

from util.ProjectRoad import getRoad

# 人脸识别模型，提取128D的特征矢量
# face recognition model, the object maps human faces into 128D vectors
# Refer this tutorial: http://dlib.net/python/index.html#dlib.face_recognition_model_v1
# 2022-02-10:修改：调整读取face的cvs时，第一列为名字

facerec = dlib.face_recognition_model_v1(getRoad() + "\\dlib\\dlib_face_recognition_resnet_model_v1.dat")


# 计算两个128D向量间的欧式距离
# compute the e-distance between two 128D features
def return_euclidean_distance(feature_1, feature_2):
    feature_1 = np.array(feature_1)
    feature_2 = np.array(feature_2)
    dist = np.sqrt(np.sum(np.square(feature_1 - feature_2)))
    return dist


# 处理存放所有人脸特征的 csv
path_features_known_csv =getRoad()+ "\\data\\features_all.csv"
csv_rd = pd.read_csv(path_features_known_csv, header=None)

# 用来存放所有录入人脸特征的数组
features_known_arr = []
# 用来存放所有录入人脸名字的数组
name_known_arr = []

# 读取已知人脸数据
# print known faces
for i in range(csv_rd.shape[0]):
    features_someone_arr = []
    name_known_arr.append(csv_rd.loc[i, :][0])
    for j in range(1, len(csv_rd.loc[i, :])):
        features_someone_arr.append(csv_rd.loc[i, :][j])
    features_known_arr.append(features_someone_arr)

print("Faces in Database：", len(features_known_arr))

# Dlib 检测器和预测器
# The detector and predictor will be used
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(getRoad()+'\\dlib\\shape_predictor_68_face_landmarks.dat')

# 创建 cv2 摄像头对象
# cv2.VideoCapture(0) to use the default camera of PC,
# and you can use local video name by use cv2.VideoCapture(filename)
cap = cv2.VideoCapture(0)

# cap.set(propId, value)
# 设置视频参数，propId 设置的视频参数，value 设置的参数值
cap.set(3, 480)

# cap.isOpened() 返回 true/false 检查初始化是否成功
# when the camera is open
while cap.isOpened():

    flag, img_rd = cap.read()
    kk = cv2.waitKey(1)

    # 取灰度
    img_gray = cv2.cvtColor(img_rd, cv2.COLOR_RGB2GRAY)

    # 人脸数 faces
    faces = detector(img_gray, 0)

    # 待会要写的字体 font to write later
    font = cv2.FONT_HERSHEY_COMPLEX

    # 存储当前摄像头中捕获到的所有人脸的坐标/名字
    # the list to save the positions and names of current faces captured
    pos_namelist = []
    name_namelist = []

    # 按下 q 键退出
    # press 'q' to exit
    if kk == ord('q'):
        break
    else:
        # 检测到人脸 when face detected
        if len(faces) != 0:
            # 获取当前捕获到的图像的所有人脸的特征，存储到 features_cap_arr
            # get the features captured and save into features_cap_arr
            features_cap_arr = []
            for i in range(len(faces)):
                shape = predictor(img_rd, faces[i])
                features_cap_arr.append(facerec.compute_face_descriptor(img_rd, shape))

            # 遍历捕获到的图像中所有的人脸
            # traversal all the faces in the database
            for k in range(len(faces)):
                print("##### camera person", k+1, "#####")
                # 让人名跟随在矩形框的下方
                # 确定人名的位置坐标
                # 先默认所有人不认识，是 unknown
                # set the default names of faces with "unknown"
                name_namelist.append("unknown")

                # 每个捕获人脸的名字坐标 the positions of faces captured
                pos_namelist.append(tuple([faces[k].left(), int(faces[k].bottom() + (faces[k].bottom() - faces[k].top())/4)]))

                # 对于某张人脸，遍历所有存储的人脸特征
                # for every faces detected, compare the faces in the database
                e_distance_list = []
                for i in range(len(features_known_arr)):
                    # 如果 person_X 数据不为空
                    if str(features_known_arr[i][0]) != '0.0':
                        print("with person", str(i + 1), "the e distance: ", end='')
                        e_distance_tmp = return_euclidean_distance(features_cap_arr[k], features_known_arr[i])
                        print(e_distance_tmp)
                        e_distance_list.append(e_distance_tmp)
                    else:
                        # 空数据 person_X
                        e_distance_list.append(999999999)
                # Find the one with minimum e distance
                similar_person_num = e_distance_list.index(min(e_distance_list))
                # print("Minimum e distance with person", str(int(similar_person_num)+1))
                print("Minimum e distance with person", name_known_arr[similar_person_num])

                if min(e_distance_list) < 0.4:
                    # 在这里修改 person_1, person_2 ... 的名字
                    # 可以在这里改称 Jack, Tom and others
                    # Here you can modify the names shown on the camera
                    name_namelist[k] = name_known_arr[similar_person_num]
                    print("May be person "+name_known_arr[similar_person_num])
                else:
                    print("Unknown person")

                # 矩形框
                # draw rectangle
                for kk, d in enumerate(faces):
                    # 绘制矩形框
                    cv2.rectangle(img_rd, tuple([d.left(), d.top()]), tuple([d.right(), d.bottom()]), (0, 255, 255), 2)
                print('\n')

            # 在人脸框下面写人脸名字
            # write names under rectangle
            for i in range(len(faces)):
                cv2.putText(img_rd, name_namelist[i], pos_namelist[i], font, 0.8, (0, 255, 255), 1, cv2.LINE_AA)

    print("Faces in camera now:", name_namelist, "\n")

    cv2.putText(img_rd, "Press 'q': Quit", (20, 450), font, 0.8, (84, 255, 159), 1, cv2.LINE_AA)
    cv2.putText(img_rd, "Face Recognition", (20, 40), font, 1, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(img_rd, "Faces: " + str(len(faces)), (20, 100), font, 1, (0, 0, 255), 1, cv2.LINE_AA)

    # 窗口显示 show with opencv
    cv2.imshow("camera", img_rd)

# 释放摄像头 release camera
cap.release()

# 删除建立的窗口 delete all the windows
cv2.destroyAllWindows()



