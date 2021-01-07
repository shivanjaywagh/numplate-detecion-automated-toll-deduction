import numpy as np
import cv2
import pymysql

from PIL import Image
from pytesseract import image_to_string
#conn = pymysql.connect(host = "localhost",user="root",passwd="",db="no_plate")
#myCurser = conn.cursor()
#pytesseract.pytesseract.tesseract_cmd = 'C:\Python27\Lib\site-packages\pytesseract'
x = 'temp.jpg'
img=cv2.imread(x)
"""
#Graying the image
img=cv2.imread('temp.jpg')
img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
bimg=cv2.blur(img,(3,3))
cv2.imshow('out',bimg)
"""
#(image,threshold level,maximum value to be applied,method)
(T,thresh)=cv2.threshold(img,155,255,cv2.THRESH_BINARY)
cv2.imshow('out1',thresh)
"""
	#Median Blur
img_noise = img + np.random.uniform(-20,20,size=np.shape(img))
cv2.imwrite('plate8.png',img_noise)
median = cv2.medianBlur(img_noise.astype(np.uint8),(3),0)
cv2.imshow('Median Blur',median)
"""

img1 = Image.open(x)	
text=image_to_string(img1, lang = 'eng')
print(text)
text = text.replace(" ", "")
text = text.replace(".", "")
text = text.replace("\n", "")
print(text)	
cv2.waitKey()
cv2.destroyAllWindows()
"""
myCurser.execute("select Addhar_no from vehical_detail where NO_plate=%s",text)
myresult = myCurser.fetchone()
print(myresult)
myCurser.execute("select Amount from bank_addhar_detail where Addhar_no=%s",myresult)
myresult1 = myCurser.fetchone()
print(myresult1)
myresult1 = [int(_) for _ in myresult1]
myresult1 -= 50
myCurser.execute("select Amount_t from toll_detail")
myresult11 = myCurser.fetchone()
myresult11=myresult11+50
print(myresult11)

print("SQL query fired..!")
conn.commit()
conn.close
"""