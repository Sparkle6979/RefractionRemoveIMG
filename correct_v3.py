import numpy as np
import cv2


def refract_correct(img, water_refractive_index, f):
    # 图像大小
    height, width = img.shape[:2]

    # 生成网格点
    x, y = np.meshgrid(np.arange(width), np.arange(height))
    pixel_coords = np.stack([x, y, np.ones_like(x)], axis=-1)

    # 相机内参
    K = np.array([[f, 0, width/2], [0, f, height/2], [0, 0, 1]])

    # 计算每个像素的光线经过水面折射后的方向
    cam_ray = np.linalg.inv(K) @ pixel_coords
    cam_ray = cam_ray / np.linalg.norm(cam_ray, axis=-1, keepdims=True)
    
    # 计算折射角度
    air_refractive_index = 1.0
    cos_theta1 = -cam_ray[..., -1]
    cos_theta2 = np.sqrt(1 - (air_refractive_index / water_refractive_index)**2 * (1 - cos_theta1**2))
    
    # 水下部分光线的方向向量，即折射部分
    refract_ray = (air_refractive_index / water_refractive_index) * cam_ray[..., :-1] + cos_theta2[..., None] * np.array([0, 0, -1])
    
    # 计算每个像素的折射点
    t = -cam_ray[..., -1] / refract_ray[..., -1]
    refract_coords = pixel_coords[..., :-1] + t[..., None] * refract_ray[..., :-1]

    # 双线性插值采样
    refract_coords = np.round(refract_coords).astype(int)
    refract_coords = np.clip(refract_coords, 0, np.array([width-1, height-1]))
    refracted_img = img[refract_coords[..., 1], refract_coords[..., 0]]

    return refracted_img



img = cv2.imread('./col.jpg')

# # 显示图片
# cv2.imshow("image", img)


img = refract_correct(img,1.33,10)
print(img.shape)
# cv2.waitKey(0)
# cv2.destroyAllWindows()