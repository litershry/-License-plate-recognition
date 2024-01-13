import cv2 
import numpy as np
def rec_car(img_name):
    img_r = cv2.imread(img_name)
    img_resize = cv2.resize(img_r,(640,480), )
    # 高斯模糊+中值滤波
    img_gaus = cv2.GaussianBlur(img_resize, (5, 5), 0)  # 高斯模糊
    img_med = cv2.medianBlur(img_gaus, 5)  # 中值滤波

    # 设定阈值
    lower_blue = np.array([100, 40,50])
    upper_blue = np.array([140, 255, 255])
    lower_yellow = np.array([15, 55, 55])
    upper_yellow = np.array([50, 255, 255])
    lower_green = np.array([0, 3, 116])
    upper_green = np.array([76, 211, 255])

# 转换为HSV
    hsv = cv2.cvtColor(img_med, cv2.COLOR_BGR2HSV)

# 根据阈值构建掩膜
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)  
    mask_green = cv2.inRange(hsv, lower_green, upper_green)  

# 对原图像和掩膜进行位运算
# src1：第一个图像（合并的第一个对象）src2：第二个图像（合并的第二个对象）mask：理解为要合并的规则。
    img_blue = cv2.bitwise_and(img_med, img_med, mask=mask_blue)
    img_yellow = cv2.bitwise_and(img_med, img_med, mask=mask_yellow)
    img_green = cv2.bitwise_and(img_med, img_med, mask=mask_green)



    # 灰度化+二值化
    img_gray_h = cv2.cvtColor(img_blue, cv2.COLOR_BGR2GRAY)  # 转换了灰度化
    # img_gray_h = cv2.cvtColor(img_yellow, cv2.COLOR_BGR2GRAY)  # 转换了灰度化
    # img_gray_h = cv2.cvtColor(img_green, cv2.COLOR_BGR2GRAY)  # 转换了灰度化
    ret1, img_thre_h = cv2.threshold(img_gray_h, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)


    # 进行Sobel算子运算，直至二值化
    img_gray_s = cv2.cvtColor(img_med, cv2.COLOR_BGR2GRAY)

    # sobel算子运算
    img_sobel_x = cv2.Sobel(img_gray_s, cv2.CV_32F, 1, 0, ksize=3)  # x轴Sobel运算
    img_sobel_y = cv2.Sobel(img_gray_s, cv2.CV_32F, 0, 1, ksize=3)
    img_ab_y = np.uint8(np.absolute(img_sobel_y))
    img_ab_x = np.uint8(np.absolute(img_sobel_x))  # 像素点取绝对值
    img_ab = cv2.addWeighted(img_ab_x, 0.5, img_ab_y, 0.5, 0)  # 将两幅图像叠加在一起（按一定权值）
    # 考虑再加一次高斯去噪
    img_gaus_1 = cv2.GaussianBlur(img_ab, (5, 5), 0)  # 高斯模糊


    # 二值化操作
    ret2, img_thre_s = cv2.threshold(img_gaus_1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)  # 正二值化


    # 颜色空间与边缘算子的图像互相筛选
    # 同时遍历两幅二值图片，若两者均为255，则置255
    img_1 = np.zeros(img_thre_h.shape, np.uint8)  # 重新拷贝图片
    height = img_resize.shape[0]  # 行数
    width = img_resize.shape[1]  # 列数
    for i in range(height):
        for j in range(width):
            h = img_thre_h[i][j]
            s = img_thre_s[i][j]
            if h == 255 and s == 255:
                img_1[i][j] = 255
            else:
                img_1[i][j] = 0
    # cv.imshow('threshold',img_1)
    # cv.waitKey(0)


    # 二值化后的图像进行闭操作
    kernel = np.ones((14, 18), np.uint8)
    img_close = cv2.morphologyEx(img_1, cv2.MORPH_CLOSE, kernel)  # 闭操作
    img_med_2 = cv2.medianBlur(img_close, 5)
    # cv.imshow('close',img_med_2)
    # cv.waitKey(0)

    # 查找轮廓
    regions = []  # 区域
    list_rate = []
    img_input = img_med_2.copy()
    img_input,contours, hierarchy = cv2.findContours(img_input, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #   筛选面积最小的
    for contour in contours:
        # 计算该轮廓的面积
        area = cv2.contourArea(contour)
        # 面积小的都筛选掉
        if area < 500:
            continue
        # 轮廓近似,epsilon，是从轮廓到近似轮廓的最大距离。是一个准确率参数，好的epsilon的选择可以得到正确的输出。True决定曲线是否闭合。
        epslion = 1e-3 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epslion, True)  # 曲线折线化
        # 找到最小的矩形，该矩形可能有方向
        rect = cv2.minAreaRect(contour)
        # box是四个点的坐标
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        # 计算高和宽
        height = abs(box[0][1] - box[2][1])
        width = abs(box[0][0] - box[2][0])
        # 车牌正常情况下长高比为2-5之间（精确一点可为（2.2,3.6））
        ratio = float(width) / float(height)
        if ratio > 2 and ratio < 5:
            regions.append(box)
            list_rate.append(ratio)
    # 输出车牌的轮廓
    #print('[INF0]:图中检测到车牌数：%d' % len(regions))  # 输出疑似车牌图块的数量
    # index = getSatifyestBox(list_rate)
    # region = regions[index]
    # 用绿线画出这些找到的轮廓
    # 重新申请空间拷贝，因为drawcontours会改变原图片因为drawcontours会改变原图片
    img_2 = np.zeros(img_resize.shape, np.uint8)
    img_2 = img_resize.copy()
    # print(regions)
    for boxf in regions:
        x, y, w, h = cv2.boundingRect(boxf)
        cv2.rectangle(img_2,(x,y),(x+w,y+h),(0,255,0),2)
        #cv2.drawContours(img_2, [boxf], 0, [0, 255, 0], 2)
        img_3 = cv2.resize(img_2[y:y+h,x:x+w], (560,150), 3)
        return img_3
    # cv2.resize(img, (150, 70), fx=0.25, fy=0.25, interpolation=cv2.INTER_NEAREST)
    
