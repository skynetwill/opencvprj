import cv2
import numpy as np
import glob
import matplotlib.pyplot as plt


# 1. 相机标定（获取相机内参和畸变系数）
def camera_calibration(calib_images_path, chessboard_size):
    """
    进行相机标定，获取相机内参矩阵和畸变系数
    :param calib_images_path: 标定图像路径模式
    :param chessboard_size: 棋盘格内角点数量 (width, height)
    :return: 相机矩阵, 畸变系数
    """
    # 准备对象点：棋盘格上的3D点 (0,0,0), (1,0,0), (2,0,0) ....,(8,5,0)
    objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)

    # 存储所有图像的对象点和图像点
    objpoints = []  # 真实世界中的3D点
    imgpoints = []  # 图像中的2D点

    # 获取所有标定图像
    images = glob.glob(calib_images_path)

    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 查找棋盘格角点
        ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)

        # 如果找到，添加对象点和图像点
        if ret:
            objpoints.append(objp)

            # 提高角点检测精度
            corners_refined = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1),
                                               (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001))
            imgpoints.append(corners_refined)

    # 相机标定
    ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(
        objpoints, imgpoints, gray.shape[::-1], None, None)

    return camera_matrix, dist_coeffs


# 2. 矩形检测与角点提取
def detect_rectangle(image):
    """
    检测图像中的矩形并提取角点
    :param image: 输入图像
    :return: 矩形角点坐标（有序）
    """
    # 转换为灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 高斯模糊
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # 边缘检测
    edges = cv2.Canny(blurred, 50, 150)

    # 形态学操作闭合边缘
    kernel = np.ones((5, 5), np.uint8)
    edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

    # 查找轮廓
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 筛选最大轮廓（假设矩形是图像中最大的轮廓）
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)

        # 多边形近似
        epsilon = 0.02 * cv2.arcLength(largest_contour, True)
        approx = cv2.approxPolyDP(largest_contour, epsilon, True)

        # 确保是四边形
        if len(approx) == 4:
            # 对四个角点进行排序：左上，右上，右下，左下
            points = approx.reshape(4, 2)
            rect_points = order_points(points)
            return rect_points

    return None


def order_points(points):
    """
    对矩形四个角点进行排序：左上，右上，右下，左下
    """
    # 按照x+y的大小排序，最小的是左上，最大的是右下
    s = points.sum(axis=1)
    rect = np.zeros((4, 2), dtype="float32")

    rect[0] = points[np.argmin(s)]  # 左上
    rect[2] = points[np.argmax(s)]  # 右下

    # 按照y-x的大小排序，最小的是右上，最大的是左下
    diff = np.diff(points, axis=1)
    rect[1] = points[np.argmin(diff)]  # 右上
    rect[3] = points[np.argmax(diff)]  # 左下

    return rect


# 3. 位姿解算与可视化
def solve_pnp_and_visualize(image, image_points, object_points, camera_matrix, dist_coeffs):
    """
    使用solvePnP解算位姿并进行可视化
    """
    # 使用solvePnP计算旋转和平移向量
    success, rvec, tvec = cv2.solvePnP(object_points, image_points,
                                       camera_matrix, dist_coeffs)

    if success:
        # 定义3D坐标轴长度
        axis_length = 50
        axis_points = np.float32([[0, 0, 0],  # 原点
                                  [axis_length, 0, 0],  # X轴
                                  [0, axis_length, 0],  # Y轴
                                  [0, 0, axis_length]  # Z轴
                                  ])

        # 将3D轴点投影到2D图像平面
        img_points, _ = cv2.projectPoints(axis_points, rvec, tvec,
                                          camera_matrix, dist_coeffs)

        img_points = img_points.reshape(-1, 2)

        # 获取图像上的点坐标
        origin = tuple(img_points[0].astype(int))
        x_axis = tuple(img_points[1].astype(int))
        y_axis = tuple(img_points[2].astype(int))
        z_axis = tuple(img_points[3].astype(int))

        # 绘制坐标轴
        cv2.line(image, origin, x_axis, (0, 0, 255), 5)  # X轴 (红色)
        cv2.line(image, origin, y_axis, (0, 255, 0), 5)  # Y轴 (绿色)
        cv2.line(image, origin, z_axis, (255, 0, 0), 5)  # Z轴 (蓝色)

        # 绘制矩形角点
        for i, point in enumerate(image_points):
            cv2.circle(image, tuple(point.astype(int)), 5, (255, 255, 0), -1)
            cv2.putText(image, str(i), tuple(point.astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        return image, rvec, tvec

    return image, None, None


# 主函数
def main():
    # 相机标定（如果已有标定数据，可以跳过这一步）
    # camera_matrix, dist_coeffs = camera_calibration('calibration_images/*.jpg', (9, 6))

    # 如果没有标定图像，可以使用近似值（需要根据实际相机调整）
    camera_matrix = np.array([[800, 0, 320],
                              [0, 800, 240],
                              [0, 0, 1]], dtype=np.float32)

    dist_coeffs = np.zeros((5, 1), dtype=np.float32)

    # 定义矩形在世界坐标系中的3D点坐标（单位：毫米）
    # 假设矩形尺寸为 100mm x 150mm，位于z=0平面
    rect_width = 100
    rect_height = 150
    object_points = np.array([[-rect_width / 2, -rect_height / 2, 0],  # 左下
                              [rect_width / 2, -rect_height / 2, 0],  # 右下
                              [rect_width / 2, rect_height / 2, 0],  # 右上
                              [-rect_width / 2, rect_height / 2, 0]  # 左上
                              ], dtype=np.float32)

    # 打开摄像头
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 检测矩形并获取角点
        image_points = detect_rectangle(frame)

        if image_points is not None:
            # 解算位姿并可视化
            result_frame, rvec, tvec = solve_pnp_and_visualize(
                frame.copy(), image_points, object_points, camera_matrix, dist_coeffs)

            if rvec is not None:
                # 显示位姿信息
                cv2.putText(result_frame, f"tvec: {tvec.flatten()}", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                cv2.putText(result_frame, f"rvec: {rvec.flatten()}", (10, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

            cv2.imshow('Pose Estimation', result_frame)
        else:
            cv2.imshow('Pose Estimation', frame)

        # 按'q'退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()