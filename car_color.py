import cv2
import numpy as np
def color(img_path):
    # cv2.imshow('origin', img_path)
    height = img_path.shape[0]
    width = img_path.shape[1]
    # print('面积：', height * width)

# 设定阈值
    lower_blue = np.array([100, 43, 46])
    upper_blue = np.array([124, 255, 255])
    lower_yellow = np.array([15, 55, 55])
    upper_yellow = np.array([50, 255, 255])
    lower_green = np.array([0, 3, 116])
    upper_green = np.array([76, 211, 255])

# 转换为HSV
    hsv = cv2.cvtColor(img_path, cv2.COLOR_BGR2HSV)

# 根据阈值构建掩膜
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)  #
    mask_green = cv2.inRange(hsv, lower_green, upper_green)  #

# 对原图像和掩膜进行位运算
# src1：第一个图像（合并的第一个对象）src2：第二个图像（合并的第二个对象）mask：理解为要合并的规则。
    res_blue = cv2.bitwise_and(img_path, img_path, mask=mask_blue)
    res_yellow = cv2.bitwise_and(img_path, img_path, mask=mask_yellow)
    res_green = cv2.bitwise_and(img_path, img_path, mask=mask_green)

# 显示图像
# cv2.imshow('frame', img_path)
    # cv2.imshow('mask_blue', mask_blue)
    # cv2.imshow('mask_yellow', mask_yellow)
    # cv2.imshow('mask_green', mask_green)
# cv2.imshow('res', res)

# 对mask进行操作--黑白像素点统计  因为不同颜色的掩膜面积不一样
# 记录黑白像素总和

    blue_white = 0
    blue_black = 0
    yellow_white = 0
    yellow_black = 0
    green_white = 0
    green_black = 0

# 计算每一列的黑白像素总和
    for i in range(width):
        for j in range(height):
            if mask_blue[j][i] == 255:
                blue_white += 1
            if mask_blue[j][i] == 0:
                blue_black += 1
            if mask_yellow[j][i] == 255:
                yellow_white += 1
            if mask_yellow[j][i] == 0:
                yellow_black += 1
            if mask_green[j][i] == 255:
                green_white += 1
            if mask_green[j][i] == 0:
                green_black += 1

    color_list = ['blue','yellow','green']
    num_list = [blue_white,yellow_white,green_white]
    end_color = color_list[num_list.index(max(num_list))]
    print(end_color)
    return end_color
