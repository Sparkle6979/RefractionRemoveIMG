import cv2
import numpy as np

# 生成一个黑色背景
height, width = 480, 640
img = np.zeros((height, width, 3), dtype=np.uint8)

# 定义水面的位置
water_level = 200

# 绘制水面
cv2.rectangle(img, (0, 0), (width, water_level), (255, 255, 255), -1)

# 定义石头的位置和大小
stone_center = (320, 360)
stone_radius = 80

# 绘制石头（水下部分）
cv2.circle(img, stone_center, stone_radius, (0, 0, 255), -1)
cv2.circle(img, stone_center, stone_radius, (255, 255, 255), 10)

# 绘制石头（水上部分）
cv2.circle(img, (stone_center[0], 2*water_level - stone_center[1]), stone_radius, (0, 255, 0), -1)
cv2.circle(img, (stone_center[0], 2*water_level - stone_center[1]), stone_radius, (255, 255, 255), 10)

# 显示图片
cv2.imshow("image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()