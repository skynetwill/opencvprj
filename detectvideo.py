import cv2
import numpy as np

# --- Step 1: Set up Video Capture ---
# 你可以选择两种输入方式:
# 1. 从摄像头实时捕获: video_capture = cv2.VideoCapture(0)
# 2. 从本地视频文件读取: video_capture = cv2.VideoCapture('tennis_ball.mp4')
# 请确保你有一个名为 'tennis_ball.mp4' 的视频文件在同一目录下, 或者改为摄像头输入。
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
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([40, 255, 255])

    # 根据定义的颜色范围, 创建一个二值化蒙版(mask)
    # 在这个蒙版中, 颜色范围内的像素会显示为白色, 其余为黑色
    color_mask = cv2.inRange(hsv_frame, lower_yellow, upper_yellow)

    # --- Step 3: 蒙版优化 (Mask Refinement) ---
    # 使用形态学操作来去除噪点并优化蒙版
    # 腐蚀(Erode)操作可以去除小的噪点
    kernel = np.ones((5, 5), np.uint8)
    mask_eroded = cv2.erode(color_mask, kernel, iterations=1)
    # 膨胀(Dilate)操作可以填充物体内部的空洞, 使其更完整
    mask_dilated = cv2.dilate(mask_eroded, kernel, iterations=2)

    # --- Step 4: 寻找并筛选轮廓 (Find and Filter Contours) ---
    # 在优化后的蒙版上寻找轮廓
    contours, _ = cv2.findContours(mask_dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 如果找到了轮廓, 则进行处理
    if contours:
        # 寻找面积最大的轮廓, 我们假设它就是我们的目标网球
        largest_contour = max(contours, key=cv2.contourArea)

        # 筛选: 只有当最大轮廓的面积大于一个阈值时才进行处理, 以免框选到小的噪点
        if cv2.contourArea(largest_contour) > 500:
            # --- Step 5: 多边形拟合与最小框选 (Polygon Fitting and Bounding Box) ---

            # a) 多边形拟合 (可选, 用于分析形状)
            # 我们可以用多边形拟合来判断形状是否接近圆形
            perimeter = cv2.arcLength(largest_contour, True)
            epsilon = 0.02 * perimeter
            approx = cv2.approxPolyDP(largest_contour, epsilon, True)

            # b) 最小外接旋转矩形 (Minimum Area Rectangle)
            # 这是最精确的框选方式, 它可以根据物体的方向旋转
            rect = cv2.minAreaRect(largest_contour)
            box = cv2.boxPoints(rect)
            box = np.intp(box)  # 将坐标转换为整数

            # 在原始帧上画出这个旋转矩形
            cv2.drawContours(frame, [box], 0, (0, 255, 0), 2)

            # (可选) 在矩形旁边显示一些信息, 比如顶点数
            cv2.putText(frame, f"Vertices: {len(approx)}", (box[1][0], box[1][1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

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
