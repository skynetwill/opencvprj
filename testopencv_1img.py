import cv2 # 导入视觉库
import numpy as np
img = cv2.imread('bill.jpg') # 把引号内的文件名修改为你的图片名
img2 = cv2.imread('robin.jpg') # 把引号内的文件名修改为你的图片名
# cv2.imshow('test', img)
# cv2.imwrite('images/robin.jpg', img)
# cv2.waitKey(0) # 显示图片直到有任何键盘点击操作

# # resize example调整大小
# print(img.shape)
# imgResize = cv2.resize(img,(224,224)) ##Decrease size
# imgResize2 = cv2.resize(img2,(800,800)) ##Increase size
# cv2.imshow("Image",img)
# cv2.imshow("Image Resize",imgResize)
# cv2.imshow("Image Increase size",imgResize2)
# print(imgResize.shape)
# cv2.waitKey(0) # 显示图片直到有任何键盘点击操作

## resize example by shape成比例调整大小
# print(img.shape)
# shape = img.shape
# imgResize = cv2.resize(img,(shape[0]//2,shape[1]//2))##Decrease size
# imgResize2 = cv2.resize(img,(shape[0]*2,shape[1]*2)) ##Increase size
# cv2.imshow("Image",img)
# cv2.imshow("Image Resize",imgResize)
# cv2.imshow("Image Increase size",imgResize2)
# print(imgResize.shape)
# cv2.waitKey(0)

## Crop image裁剪图像
# imgCropped = img[0:963,215:953]   # 在可以使⽤paint（微软自带的“画图”软件）来找到（x1， y1） ， （x2， y2） 的正确坐标。注意要转换成[y1:y2, x1:x2]
# cv2.imshow("Image cropped",imgCropped)
# cv2.imshow("Image",img)
# cv2.waitKey(0)

## convert color图像转为灰度
# imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# cv2.imshow('test', imgGray)
# # cv2.imwrite('images/robin.jpg', img)
# cv2.waitKey(0) # 显示图片直到有任何键盘点击操作

## convert color图像转为HSV,主要⽤于对象跟踪
# imgHsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
# cv2.imshow('test', imgHsv)
# # cv2.imwrite('images/robin.jpg', img)
# cv2.waitKey(0) # 显示图片直到有任何键盘点击操作

## blur image 模糊⽤于去除图像中的多余噪声， 也称为平滑， 这是对图像应⽤低通滤波器的过程
# imgBlur = cv2.GaussianBlur(img,(3,3),0)  # GaussianBlur(img,(sigmaX,sigmaY),kernalSize);
# # kernalsize − A Size object representing the size of the kernel.
# # sigmaX − A variable representing the Gaussian kernel standard deviation in X direction.
# # sigmaY - same as sigmaX
# cv2.imshow('test', imgBlur)
# # cv2.imwrite('images/robin.jpg', img)
# cv2.waitKey(0) # 显示图片直到有任何键盘点击操作

## Canny边缘检测器来检测图像中的边缘  效果是图片上的图形只剩下边了
# imgCanny = cv2.Canny(img,100,150)  #threshold1,threshold2:Different values of threshold different for every images
# cv2.imshow('test', imgCanny)
# # cv2.imwrite('images/robin.jpg', img)
# cv2.waitKey(0) # 显示图片直到有任何键盘点击操作

## Dilate膨胀是⽤来增加图像中边缘的⼤⼩
# imgCanny = cv2.Canny(img,100,150)  #threshold1,threshold2:Different values of threshold different for every images
# kernel = np.ones((5,5),np.uint8) ## DEFINING KERNEL OF 5x5
# imgDilation = cv2.dilate(imgCanny,kernel,iterations=1) ##DILATION
# cv2.imshow('test', img)
# cv2.imshow('test1', imgCanny)
# cv2.imshow('test2', imgDilation)
# # cv2.imwrite('images/robin.jpg', img)
# cv2.waitKey(0) # 显示图片直到有任何键盘点击操作

## Erode 腐蚀是扩张的反⾯， 它⽤于减⼩图像边缘的尺⼨
# imgCanny = cv2.Canny(img,100,150)  #threshold1,threshold2:Different values of threshold different for every images
# kernel = np.ones((5,5),np.uint8) ## DEFINING KERNEL OF 5x5
# # imgDilation = cv2.dilate(imgCanny,kernel,iterations=1) ##DILATION
# imgErosion = cv2.erode(img,kernel,iterations=1) ##EROSION
# cv2.imshow('test', img)
# cv2.imshow('test1', imgCanny)
# cv2.imshow('test2', imgErosion)
# # cv2.imwrite('images/robin.jpg', img)
# cv2.waitKey(0) # 显示图片直到有任何键盘点击操作


# 绘制矩形cv2.rectangle(img,(x1,y1),(x2,y2),(R,G,B),THICKNESS)
# R,G,B: color in RGB form (255,255,0)
# THICKNESS: thickness of rectangel(integer)
# cv2.rectangle(img,(100,200),(200,300),(255,0,255),1)
#
# # 绘制圆形cv2.circle(img,(x,y),radius,(R,G,B),
# cv2.circle(img,(200,130),90,(255,255,0),2)
#
# # 绘制直线cv2.line(img,(x1,y1),(x2,y2),(R,G,B),THICKNESS)
# cv2.line(img,(110,260),(300,260),(0,255,0),3)
#
# # 书写文字cv2.putText(img,text,(x,y),FONT,FONT_SCALE,(R,G,B),THICKNESS)
# cv2.putText(img,"HELLO",(120,250),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
#
# cv2.imshow('test', img)
# # cv2.imshow('test1', imgCanny)
# # cv2.imshow('test2', imgErosion)
# # # cv2.imwrite('images/robin.jpg', img)
# cv2.waitKey(0) # 显示图片直到有任何键盘点击操作

# 检测并裁剪脸部
# Load the cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# Read the input image
# img = cv2.imread('images/img0.jpg')
img = cv2.imread('bill.jpg') # 把引号内的文件名修改为你的图片名
# Convert into grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# Detect faces
faces = face_cascade.detectMultiScale(gray, 1.3, 4)
# Draw rectangle around the faces
for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
    # Cropping Face
    crop_face = img[y:y + h, x:x + w]
    #Saving Cropped Face
    cv2.imwrite(str(w) + str(h) + '_faces.jpg', crop_face)
cv2.imshow('img', img)
cv2.imshow("imgcropped",crop_face)
cv2.waitKey()


