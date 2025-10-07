import cv2
import numpy as np

# --- 步骤 1: 准备工作 ---
# 1. 打印一个矩形: 在一张白纸上清晰地打印或画一个矩形。
# 2. 测量尺寸: 精确测量你打印的矩形的长和宽（单位：毫米）。
#    例如: width = 150mm, height = 100mm
# 3. 相机标定: (极其重要!) 运行一个相机标定程序来获取你摄像头的内参矩阵和畸变系数。
#    如果你没有，可以使用下面的通用值，但这会导致姿态估计不准确。

# --- 步骤 2: 定义参数 ---

# 1. 相机内参矩阵 (Camera Matrix) 和 畸变系数 (Distortion Coefficients)
# !!! 警告: 下面的值是通用示例，你必须用自己标定得到的值替换它们以获得准确结果 !!!
# 你可以使用OpenCV的标定功能或Matlab标定工具箱来获取这些值。
CAMERA_MATRIX = np.array([
    [650.0, 0.0, 320.0],  # fx, 0, cx
    [0.0, 650.0, 240.0],  # 0, fy, cy
    [0.0, 0.0, 1.0]  # 0, 0, 1
], dtype=np.float32)

DIST_COEFFS = np.array([0.0, 0.0, 0.0, 0.0, 0.0], dtype=np.float32)  # 通常k1, k2, p1, p2, k3

# 2. 物体的真实世界坐标 (3D Object Points)
# 根据你测量的矩形尺寸来定义。单位是毫米。
# 我们定义世界坐标系的原点(0,0,0)在矩形的左上角。
# X轴沿宽度方向，Y轴沿高度方向，Z轴垂直于纸面向外。
RECTANGLE_WIDTH_MM = 150.0
RECTANGLE_HEIGHT_MM = 100.0

# 矩形四个角点的3D坐标
OBJECT_POINTS = np.array([
    [0.0, 0.0, 0.0],  # 左上角 (原点)
    [RECTANGLE_WIDTH_MM, 0.0, 0.0],  # 右上角
    [RECTANGLE_WIDTH_MM, RECTANGLE_HEIGHT_MM, 0.0],  # 右下角
    [0.0, RECTANGLE_HEIGHT_MM, 0.0]  # 左下角
], dtype=np.float32)

# 3. 用于可视化的3D坐标轴 (3D Axis Points)
# 我们将从原点(0,0,0)画出三条轴，长度可以自定义
AXIS_LENGTH = 75.0
AXIS_POINTS = np.array([
    [0.0, 0.0, 0.0],  # 原点
    [AXIS_LENGTH, 0.0, 0.0],  # X轴终点 (红色)
    [0.0, AXIS_LENGTH, 0.0],  # Y轴终点 (绿色)
    [0.0, 0.0, -AXIS_LENGTH]  # Z轴终点 (蓝色) 注意是-Z, 因为Z轴垂直纸面向外
], dtype=np.float32)


# --- 辅助函数: 对检测到的角点进行排序 ---
def order_points(pts):
    # 初始化一个列表，用于存储排序后的四个点：
    # 0:左上, 1:右上, 2:右下, 3:左下
    rect = np.zeros((4, 2), dtype="float32")

    # 左上角的点 x+y 最小, 右下角的点 x+y 最大
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    # 右上角的点 y-x 最小, 左下角的点 y-x 最大
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    return rect


# --- 主程序 ---
# 打开摄像头
video_capture = cv2.VideoCapture(0)
if not video_capture.isOpened():
    print("错误: 无法打开摄像头。")
    exit()

while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    # --- 步骤 3: 图像处理与矩形检测 ---
    # 转换为灰度图
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 使用自适应阈值进行二值化, 以适应不同光照条件
    # 注意: 你的矩形应该是深色线条在浅色背景上
    binary_frame = cv2.adaptiveThreshold(
        gray_frame, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, 11, 2
    )

    # 寻找轮廓
    contours, _ = cv2.findContours(binary_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # 按面积对轮廓进行排序, 找到最大的轮廓
        contours = sorted(contours, key=cv2.contourArea, reverse=True)

        # 遍历轮廓, 寻找第一个符合条件的矩形
        for contour in contours:
            # 多边形拟合, 判断是否是四边形
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)

            if len(approx) == 4 and cv2.isContourConvex(approx):
                # 找到了一个四边形, 我们假设这就是我们的目标矩形

                # --- 步骤 4: 位姿解算 ---
                # 获取图像中的2D角点
                image_points_unordered = approx.reshape((4, 2)).astype(np.float32)

                # 对角点进行排序, 使其与OBJECT_POINTS的顺序对应
                image_points_ordered = order_points(image_points_unordered)

                # 使用 solvePnP
                success, rvec, tvec = cv2.solvePnP(
                    OBJECT_POINTS, image_points_ordered, CAMERA_MATRIX, DIST_COEFFS
                )

                if success:
                    # --- 步骤 5: 可视化 ---
                    # 将3D坐标轴投影到2D图像平面
                    projected_axis_points, _ = cv2.projectPoints(
                        AXIS_POINTS, rvec, tvec, CAMERA_MATRIX, DIST_COEFFS
                    )

                    # 转换坐标为整数
                    projected_axis_points = np.int32(projected_axis_points).reshape(-1, 2)

                    # 绘制坐标轴
                    origin = tuple(projected_axis_points[0])
                    x_axis_end = tuple(projected_axis_points[1])
                    y_axis_end = tuple(projected_axis_points[2])
                    z_axis_end = tuple(projected_axis_points[3])

                    cv2.line(frame, origin, x_axis_end, (0, 0, 255), 3)  # X轴: 红色
                    cv2.line(frame, origin, y_axis_end, (0, 255, 0), 3)  # Y轴: 绿色
                    cv2.line(frame, origin, z_axis_end, (255, 0, 0), 3)  # Z轴: 蓝色

                # 只处理第一个找到的矩形, 跳出循环
                break

    # 显示结果
    cv2.imshow("Pose Estimation", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放资源
video_capture.release()
cv2.destroyAllWindows()