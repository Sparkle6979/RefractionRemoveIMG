import numpy as np
import cv2

def refract_correct(img,water_refractive_index,K):
    # 图像大小
    height, width = img.shape[:2]
    
    # 生成网格点
    x, y = np.meshgrid(np.arange(width), np.arange(height))
    pixel_coords = np.stack([x, y, np.ones_like(x)], axis=-1)

    # 计算相机内参
    K_inv = np.linalg.inv(K)
   
    # 得到每一个像素点在相机坐标系下的方向向量
    cam_ray = np.matmul(K_inv, pixel_coords.reshape(-1, 3).T).T.reshape(pixel_coords.shape)
    # 进行归一化
    cam_ray_norm = cam_ray / np.linalg.norm(cam_ray, axis=-1, keepdims=True)
    

    # 折射角度的计算
    air_refractive_index = 1.0
    sin_theta1 = cam_ray_norm[..., -1]
    
    sin_theta2 = air_refractive_index / water_refractive_index * sin_theta1

    # 水下部分光线的方向向量，即折射部分角度的计算
    # TODO： 完善并改进此计算方法
    refract_ray = air_refractive_index / water_refractive_index * cam_ray
    
    # 计算折射光线部分对应的像素 coord
    refract_coords = np.matmul(K,refract_ray.reshape(-1,3).T).T.reshape(pixel_coords.shape)

    # 取整
    refract_coords = np.round(refract_coords).astype(int)

    # 范围划分
    new_r = np.clip(refract_coords, 0, np.array([width-1, height-1,1]))

    # 像素替换 TODO: 采用其他的插值方法
    refracted_img = img[new_r[..., 1], new_r[..., 0]]

    return refracted_img