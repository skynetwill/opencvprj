import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def detect_arrow_lights(image_path):
    # 1. 读取图像
    img = cv2.imread(image_path)
    if img is None:
        print(f"错误: 无法读取图像 {image_path}")
        return None, None

    # 2. 转换为灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 3. 自适应二值化
    binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 11, 2)

    # 4. 形态学操作
    kernel = np.ones((3, 3), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

    # 5. 轮廓检测
    contours, _ = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    # 6. 筛选轮廓
    arrow_contours = []
    for contour in contours:
        # 面积筛选
        area = cv2.contourArea(contour)
        if area < 800 or area > 2000:
            continue

        # 多边形拟合
        peri = cv2.arcLength(contour, True)

        # 尝试多种拟合精度
        for epsilon_factor in [0.02, 0.03, 0.04]:
            epsilon = epsilon_factor * peri
            approx = cv2.approxPolyDP(contour, epsilon, True)

            # 顶点数筛选 (5-7个顶点)
            if 5 <= len(approx) <= 8:
                # 计算轮廓的宽高比
                rect = cv2.minAreaRect(approx)
                width, height = rect[1]
                aspect_ratio = max(width, height) / min(width, height) if min(width, height) > 0 else 0

                # 箭头通常有较大的宽高比
                if aspect_ratio > 2.0:
                    arrow_contours.append(approx)
                    break

    # 7. 位置约束 - 确保检测到四个角点
    height, width = img.shape[:2]
    quadrant_arrows = [[] for _ in range(4)]  # 四个象限

    for contour in arrow_contours:
        # 计算轮廓中心
        M = cv2.moments(contour)
        if M["m00"] == 0:
            continue
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])

        # 确定轮廓所在象限
        if cx < width / 2 and cy < height / 2:
            quadrant_arrows[0].append(contour)  # 左上
        elif cx >= width / 2 and cy < height / 2:
            quadrant_arrows[1].append(contour)  # 右上
        elif cx < width / 2 and cy >= height / 2:
            quadrant_arrows[2].append(contour)  # 左下
        else:
            quadrant_arrows[3].append(contour)  # 右下

    # 8. 在每个象限中选择最可能的箭头
    final_arrows = []
    for i, quadrant in enumerate(quadrant_arrows):
        if quadrant:
            # 选择面积最大的轮廓
            largest_contour = max(quadrant, key=cv2.contourArea)
            final_arrows.append(largest_contour)
        else:
            print(f"警告: 未检测到第{i + 1}象限的箭头灯条")

    # 9. 绘制结果 - 修复np.int0错误
    result_img = img.copy()
    for i, contour in enumerate(final_arrows):
        # 绘制最小外接矩形
        rect = cv2.minAreaRect(contour)
        box = cv2.boxPoints(rect)
        # 修复: 使用astype(np.int32)替代np.int0
        box = box.astype(np.int32)
        cv2.drawContours(result_img, [box], 0, (0, 0, 255), 2)

        # 标注象限
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            quadrant_names = ["左上", "右上", "左下", "右下"]
            cv2.putText(result_img, quadrant_names[i], (cx - 20, cy - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return result_img, final_arrows


# 辅助函数：显示处理过程中的中间结果
def show_processing_steps(image_path):
    img = cv2.imread(image_path)
    if img is None:
        print("无法读取图像")
        return

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 自适应二值化
    binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 11, 2)

    # 形态学操作
    kernel = np.ones((3, 3), np.uint8)
    binary_processed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    binary_processed = cv2.morphologyEx(binary_processed, cv2.MORPH_OPEN, kernel)

    # 显示中间结果
    plt.figure(figsize=(15, 10))

    plt.subplot(2, 2, 1)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title('原始图像')
    plt.axis('off')

    plt.subplot(2, 2, 2)
    plt.imshow(gray, cmap='gray')
    plt.title('灰度图像')
    plt.axis('off')

    plt.subplot(2, 2, 3)
    plt.imshow(binary, cmap='gray')
    plt.title('二值化图像')
    plt.axis('off')

    plt.subplot(2, 2, 4)
    plt.imshow(binary_processed, cmap='gray')
    plt.title('形态学处理后的图像')
    plt.axis('off')

    plt.tight_layout()
    plt.show()


# 增强版检测函数：使用颜色信息辅助检测
def enhanced_arrow_detection(image_path):
    # 1. 读取图像
    img = cv2.imread(image_path)
    if img is None:
        return None, None

    # 2. 转换为HSV颜色空间
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 3. 根据箭头灯条的颜色设置阈值（假设灯条为蓝色）
    lower_blue = np.array([90, 50, 50])
    upper_blue = np.array([130, 255, 255])

    # 4. 创建颜色掩膜
    color_mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # 5. 形态学操作
    kernel = np.ones((5, 5), np.uint8)
    color_mask = cv2.morphologyEx(color_mask, cv2.MORPH_CLOSE, kernel)
    color_mask = cv2.morphologyEx(color_mask, cv2.MORPH_OPEN, kernel)

    # 6. 结合颜色和边缘信息
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    combined_mask = cv2.bitwise_or(color_mask, edges)

    # 7. 轮廓检测
    contours, _ = cv2.findContours(combined_mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    # 8. 筛选轮廓
    arrow_contours = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area < 100 or area > 3000:
            continue

        # 多边形拟合
        peri = cv2.arcLength(contour, True)
        epsilon = 0.03 * peri
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # 顶点数筛选
        if 5 <= len(approx) <= 8:
            # 计算轮廓的宽高比
            rect = cv2.minAreaRect(approx)
            width, height = rect[1]
            aspect_ratio = max(width, height) / min(width, height) if min(width, height) > 0 else 0

            # 箭头通常有较大的宽高比
            if aspect_ratio > 1.8:
                arrow_contours.append(approx)

    # 9. 位置约束
    height, width = img.shape[:2]
    quadrant_arrows = [[] for _ in range(4)]

    for contour in arrow_contours:
        M = cv2.moments(contour)
        if M["m00"] == 0:
            continue
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])

        if cx < width / 2 and cy < height / 2:
            quadrant_arrows[0].append(contour)
        elif cx >= width / 2 and cy < height / 2:
            quadrant_arrows[1].append(contour)
        elif cx < width / 2 and cy >= height / 2:
            quadrant_arrows[2].append(contour)
        else:
            quadrant_arrows[3].append(contour)

    # 10. 选择每个象限的最佳轮廓
    final_arrows = []
    for quadrant in quadrant_arrows:
        if quadrant:
            # 选择面积最大且宽高比最大的轮廓
            best_contour = max(quadrant, key=lambda c: cv2.contourArea(c) *
                                                       (max(cv2.minAreaRect(c)[1]) / min(cv2.minAreaRect(c)[1]) if min(
                                                           cv2.minAreaRect(c)[1]) > 0 else 0))
            final_arrows.append(best_contour)

    # 11. 绘制结果
    result_img = img.copy()
    for i, contour in enumerate(final_arrows):
        rect = cv2.minAreaRect(contour)
        box = cv2.boxPoints(rect)
        box = box.astype(np.int32)  # 修复: 使用astype(np.int32)
        cv2.drawContours(result_img, [box], 0, (0, 0, 255), 2)

        M = cv2.moments(contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            quadrant_names = ["左上", "右上", "左下", "右下"]
            cv2.putText(result_img, quadrant_names[i], (cx - 20, cy - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return result_img, final_arrows


# 交互式参数调整函数
def interactive_threshold_adjustment(image_path):
    img = cv2.imread(image_path)
    if img is None:
        return

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    def update_threshold(val):
        _, binary = cv2.threshold(gray, val, 255, cv2.THRESH_BINARY)
        cv2.imshow('Threshold Adjustment', binary)

    cv2.namedWindow('Threshold Adjustment')
    cv2.createTrackbar('Threshold', 'Threshold Adjustment', 128, 255, update_threshold)
    update_threshold(128)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# 主程序
if __name__ == "__main__":
    image_path = "exchange_station.png"  # 替换为实际图像路径

    # 检查图像路径
    if not os.path.exists(image_path):
        print(f"错误: 图像路径不存在: {image_path}")
        print("请确保图像文件存在，并提供正确的路径")
        exit(1)

    # 显示处理步骤
    print("显示图像处理中间步骤...")
    show_processing_steps(image_path)

    # 执行箭头检测
    print("执行箭头灯条检测...")
    result, arrows = detect_arrow_lights(image_path)

    if result is not None:
        print(f"检测到 {len(arrows)} 个箭头灯条")

        # 显示结果
        plt.figure(figsize=(10, 8))
        plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
        plt.title('箭头灯条检测结果')
        plt.axis('off')
        plt.show()

        # 保存结果
        cv2.imwrite("arrow_detection_result.png", result)
        print("结果已保存为 arrow_detection_result.png")

        # 如果检测到的箭头不足4个，尝试增强版检测
        if len(arrows) < 4:
            print("检测到的箭头不足4个，尝试增强版检测...")
            enhanced_result, enhanced_arrows = enhanced_arrow_detection(image_path)

            if enhanced_result is not None:
                print(f"增强版检测到 {len(enhanced_arrows)} 个箭头灯条")

                plt.figure(figsize=(10, 8))
                plt.imshow(cv2.cvtColor(enhanced_result, cv2.COLOR_BGR2RGB))
                plt.title('增强版箭头灯条检测结果')
                plt.axis('off')
                plt.show()

                cv2.imwrite("enhanced_arrow_detection_result.png", enhanced_result)
                print("增强版结果已保存为 enhanced_arrow_detection_result.png")
    else:
        print("检测失败")

        # 提供交互式阈值调整
        print("尝试交互式阈值调整...")
        interactive_threshold_adjustment(image_path)