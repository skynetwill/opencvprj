import cv2
import numpy as np
import math

# --- Step 1: Set up Video Capture ---
# 你可以选择两种输入方式:
# 1. 从摄像头实时捕获: video_capture = cv2.VideoCapture(0)
# 2. 从本地视频文件读取: video_capture = cv2.VideoCapture('tennis_ball_with_player.mp4')
# 请确保你有一个名为 'tennis_ball_with_player.mp4' 的视频文件在同一目录下, 或者改为摄像头输入。
video_capture = cv2.VideoCapture('tennis_ball.mp4')

# 检查视频是否成功打开
if not video_capture.isOpened():
    print("错误: 无法打开视频文件或摄像头。")
    exit()

# --- 新增: 用于跟踪的变量 ---
# 记录上一帧检测到的球的位置
last_known_position = None
# 连续多少帧没有检测到球的计数器
frames_without_detection = 0

# --- 主循环: 逐帧处理视频 ---
while True:
    # 读取当前帧
    ret, frame = video_capture.read()

    if not ret:
        print("视频播放完毕或无法读取帧。")
        break

    # --- Step 2: 多范围颜色分割 (Multi-Range Color Segmentation) ---
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # **修正1: 定义两个颜色范围**
    # 范围1: 捕捉鲜艳的亮黄色 (类似之前)
    bright_lower_yellow = np.array([22, 120, 150])
    bright_upper_yellow = np.array([38, 255, 255])
    bright_mask = cv2.inRange(hsv_frame, bright_lower_yellow, bright_upper_yellow)

    # 范围2: 捕捉因运动模糊或阴影而变暗的黄色 (S和V的下限更低)
    dull_lower_yellow = np.array([20, 70, 100])
    dull_upper_yellow = np.array([40, 255, 255])
    dull_mask = cv2.inRange(hsv_frame, dull_lower_yellow, dull_upper_yellow)

    # **合并两个蒙版**
    combined_mask = cv2.bitwise_or(bright_mask, dull_mask)

    # --- Step 3: 蒙版优化 (Mask Refinement) ---
    kernel = np.ones((5, 5), np.uint8)
    # 闭运算填充内部空洞
    mask_dilated = cv2.dilate(combined_mask, kernel, iterations=2)
    mask_closed = cv2.erode(mask_dilated, kernel, iterations=2)

    # --- Step 4: 寻找并筛选轮廓 ---
    contours, _ = cv2.findContours(mask_closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    ball_found_in_frame = False
    if contours:
        # 我们假设面积最大的那个符合条件的轮廓是球
        contours = sorted(contours, key=cv2.contourArea, reverse=True)

        for contour in contours:
            area = cv2.contourArea(contour)
            # 调整面积范围
            if 10 < area < 500:
                perimeter = cv2.arcLength(contour, True)
                if perimeter > 0:
                    circularity = (4 * math.pi * area) / (perimeter * perimeter)
                    # 再次放宽圆形度, 因为合并后的蒙版可能形状更不规则
                    if circularity > 0.5:
                        # 如果找到了, 就画绿框并更新信息
                        rect = cv2.minAreaRect(contour)
                        box = cv2.boxPoints(rect)
                        box = np.intp(box)
                        cv2.drawContours(frame, [box], 0, (0, 255, 0), 2)

                        # 更新状态
                        last_known_position = rect  # 保存整个旋转矩形的信息
                        frames_without_detection = 0
                        ball_found_in_frame = True
                        break  # 只处理第一个找到的球

    # --- Step 5: "记忆"与"预测"机制 ---
    if not ball_found_in_frame:
        frames_without_detection += 1
        # 如果连续跟丢的帧数不多, 并且我们有上一帧的位置
        if frames_without_detection < 15 and last_known_position is not None:
            # 在上一帧的位置画一个蓝色的预测框
            box = cv2.boxPoints(last_known_position)
            box = np.intp(box)
            cv2.drawContours(frame, [box], 0, (255, 0, 0), 2)  # 蓝色代表预测
            cv2.putText(frame, "Tracking Lost", (box[1][0] - 20, box[1][1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

    # --- Step 6: 可视化结果 ---
    cv2.imshow('Real-time Object Tracking', frame)
    cv2.imshow('Processed Mask', mask_closed)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# --- Step 7: 释放资源 ---
video_capture.release()
cv2.destroyAllWindows()

