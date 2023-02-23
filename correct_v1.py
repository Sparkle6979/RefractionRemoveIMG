import math
import numpy as np


def image_refraction_correction(img, water_refractive_index):
    """
    对水下图像进行折射校正
    :param img: 待校正的水下图像
    :param water_refractive_index: 水的折射率
    :return: 校正后的水下图像
    """
    # 获取图像的大小
    rows, cols, channels = img.shape
    # 创建一个和原始图像大小一样的新图像
    new_img = np.zeros((rows, cols, channels), dtype=np.uint8)
    # 计算图像中心点的坐标
    center_x = cols // 2
    center_y = rows // 2

    # 循环遍历图像上的每个像素
    for y in range(rows):
        for x in range(cols):
            # 计算该像素到图像中心点的距离
            dx = x - center_x
            dy = y - center_y
            distance_to_center = math.sqrt(dx ** 2 + dy ** 2)

            # 计算从该像素到目标点的光线的折射角度
            refracted_angle = get_refracted_angle(water_refractive_index, distance_to_center)

            # 计算经过折射后到达目标点的像素坐标
            refracted_x, refracted_y = get_refracted_pixel(x, y, center_x, center_y, refracted_angle)

            # 如果计算出来的像素坐标在图像范围内，则将该像素的颜色赋值给新图像
            if 0 <= refracted_x < cols and 0 <= refracted_y < rows:
                new_img[y, x] = img[refracted_y, refracted_x]

    return new_img

def get_refracted_angle(water_refractive_index, distance_to_center):
    """
    计算从图像中心点到目标点的光线在水中的折射角度
    :param water_refractive_index: 水的折射率
    :param distance_to_center: 目标点到图像中心点的距离
    :return: 光线在水中的折射角度
    """
    # 计算光线在水中的入射角度
    angle_of_incidence = math.atan(distance_to_center / FOCAL_LENGTH)
    # 计算光线在水中的折射角度
    angle_of_refraction = math.asin(math.sin(angle_of_incidence) / water_refractive_index)
    return angle_of_refraction

def get_refracted_pixel(x, y, center_x, center_y, refracted_angle):
    """
    计算经过折射后到达目标点的像素坐标
    :param x: 原始像素的x坐标
    :param y: 原始像素的y坐标
    :param center_x: 图像中心点的x坐标
    :param center_y: 图像中心点的y
    """
