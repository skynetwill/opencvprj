import cv2
# import numpy as np
img_bgr = cv2.imread("test.png")
img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
img_h, img_s, img_v = cv2.split(img_hsv)
# 打印HSV通道的统计信息，帮助确定合适的阈值
print(f"H通道范围: {img_h.min()} - {img_h.max()}")
print(f"S通道范围: {img_s.min()} - {img_s.max()}")
print(f"V通道范围: {img_v.min()} - {img_v.max()}")

# 显示各通道图像以便分析
cv2.imshow("H Channel", img_h)
cv2.imshow("S Channel", img_s)
cv2.imshow("V Channel", img_v)

# 针对粉红色调整HSV范围
# 粉红色通常有两种情况：偏红的粉红(H:0-10)和偏紫的粉红(H:150-180)
# 创建两个范围的掩膜并合并

# 第一种粉红色范围（偏红）
# mask_h1 = cv2.inRange(img_h, 0, 10)
# mask_s1 = cv2.inRange(img_s, 50, 255)  # 降低饱和度下限以包含更多区域
# mask_v1 = cv2.inRange(img_v, 50, 255)  # 降低明度下限以包含更多区域
# mask1 = cv2.bitwise_and(mask_h1, mask_s1)
# mask1 = cv2.bitwise_and(mask1, mask_v1)

# 第二种粉红色范围（偏紫）
mask_h = cv2.inRange(img_h, 150, 180)
mask_s = cv2.inRange(img_s, 50, 255)
mask_v = cv2.inRange(img_v, 50, 255)
mask_h_and_s = cv2.bitwise_and(mask_h, mask_s)
mask = cv2.bitwise_and(mask_h_and_s, mask_v)

# 合并两个范围的掩膜
# mask = cv2.bitwise_or(mask1, mask2)

# # 对白色部分也创建一个掩膜（床头等浅色区域）
# mask_white = cv2.inRange(img_hsv, (0, 0, 200), (180, 30, 255))
# mask = cv2.bitwise_or(mask, mask_white)

# 可选：对掩膜进行形态学操作，去除噪声并填充空洞
# kernel = np.ones((5, 5), np.uint8)
# mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
# mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

img_out = cv2.bitwise_and(img_bgr, img_bgr, mask = mask)
cv2.imshow("img", img_bgr)
cv2.imshow("imghsv", img_hsv)
# cv2.imshow("H Mask 1 (Red-Pink)", mask_h1)
cv2.imshow("H Mask (Purple-Pink)", mask_h)
cv2.imshow("Combined Mask", mask)
cv2.imshow("img_out", img_out)
cv2.imwrite("img_out.png", img_out)
cv2.waitKey(0)
cv2.destroyAllWindows()