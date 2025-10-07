import cv2
import numpy as np
import math

# --- Step 1: Set up Video Capture ---
# 你可以选择两种输入方式:
# 1. 从摄像头实时捕获: video_capture = cv2.VideoCapture(0)
# 2. 从本地视频文件读取: video_capture = cv2.VideoCapture('tennis_ball_with_player.mp4')
# 请确保你有一个名为 'tennis_ball_with_player.mp4' 的视频文件在同一目录下, 或者改为摄像头输入。
# video_capture = cv2.VideoCapture('tennis_ball_2player.mp4')
video_capture = cv2.VideoCapture('tennis_ball.mp4')

# 检查视频是否成功打开
if not video_capture.isOpened():
    print("错误: 无法打开视频文件或摄像头。")
    exit()

# --- 主循环: 逐帧处理视频 ---
while True:
    # 读取当前帧
    ret, frame = video_capture.read()

    # 如果ret为False, 说明视频已结束或读取错误
    if not ret:
        print("视频播放完毕或无法读取帧。")
        break

    # --- Step 2: 颜色分割 (Color Segmentation) ---
    # 将当前帧从BGR色彩空间转换到HSV色彩空间
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 定义视频中黄色网球的HSV颜色范围
    # 这个范围可能需要根据你的视频光照和物体颜色微调
    lower_yellow = np.array([10, 100, 100])
    upper_yellow = np.array([40, 255, 255])

    # 根据定义的颜色范围, 创建一个二值化蒙版(mask)
    color_mask = cv2.inRange(hsv_frame, lower_yellow, upper_yellow)

    # --- Step 3: 蒙版优化 (Mask Refinement) ---
    # 使用形态学操作来去除噪点并优化蒙版
    kernel = np.ones((5, 5), np.uint8)
    mask_eroded = cv2.erode(color_mask, kernel, iterations=1)
    mask_dilated = cv2.dilate(mask_eroded, kernel, iterations=2)

    # --- Step 4: 寻找并筛选轮廓 (Find and Filter Contours) ---
    # 在优化后的蒙版上寻找轮廓
    contours, _ = cv2.findContours(mask_dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # *** 代码核心修改部分 ***
    # 遍历所有找到的轮廓, 而不是只找最大的
    for contour in contours:

        # 筛选1: 面积。我们寻找的是网球, 所以面积不能太大也不能太小
        area = cv2.contourArea(contour)
        if 70 < area < 500:  # 根据视频中球的大小调整这个范围

            # --- Step 5: 形状分析 (Shape Analysis) ---

            # a) 计算周长
            perimeter = cv2.arcLength(contour, True)

            # b) *** 新增筛选2: 圆形度 ***
            # 计算圆形度: (4 * pi * Area) / (Perimeter^2)
            # 一个完美的圆的圆形度是1
            if perimeter > 0:
                circularity = (4 * math.pi * area) / (perimeter * perimeter)

                # 我们只接受圆形度非常接近1的轮廓 (例如 > 0.75)
                # 这样就可以排除掉不规则的黄色上衣
                if 0.79 > circularity > 0.75:
                    # c) 最小外接旋转矩形
                    # 如果通过了所有筛选, 说明这很可能就是网球
                    rect = cv2.minAreaRect(contour)
                    box = cv2.boxPoints(rect)
                    box = np.intp(box)

                    # 在原始帧上画出这个旋转矩形
                    cv2.drawContours(frame, [box], 0, (0, 255, 0), 2)

                    # 在矩形旁边显示圆形度信息, 用于调试
                    cv2.putText(frame, f"Circ: {circularity:.2f}", (box[1][0], box[1][1] - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # --- Step 6: 可视化结果 (Visualize the Results) ---
    # 显示处理后的视频帧
    cv2.imshow('Real-time Object Tracking', frame)
    # (可选) 显示二值化蒙版, 以便调试颜色范围
    cv2.imshow('Color Mask', mask_dilated)

    # --- 退出循环 ---
    # 按下 'q' 键则退出循环
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# --- Step 7: 释放资源 ---
# 释放视频捕获对象
video_capture.release()
# 关闭所有OpenCV窗口
cv2.destroyAllWindows()

