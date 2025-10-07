import cv2  # 导入视觉库

cap = cv2.VideoCapture("F:\\shunshun\\university\\photo\\1.mp4")
while True:
    success, img = cap.read()
    if not success:
        break  # 如果读取失败，退出循环
    cv2.imshow("Video", img)
    if cv2.waitKey(1) & 0xff == ord('q'):  # key 'q' will break the loop cv2.waitKey(1): 等待1毫秒并获取按键值。& 0xff是为了确保在不同系统上只取按键的ASCII码。如果按下'q'键，则退出循环，实现手动中断播放
        break
cap.release()  # 释放视频捕获资源
cv2.destroyAllWindows()  # 关闭所有OpenCV窗口

# cap = cv2.VideoCapture(0)
# cap.set(3,640) ## Frame width
# cap.set(4,480) ## Frame Height
# cap.set(10,100) ## Brightness
# while True:
#     success, img = cap.read()
#     cv2.imshow("Video",img)
#     if cv2.waitKey(1) & 0xff == ord('q'):
#         break