import numpy as np
import cv2
import pymysql
from PIL import Image
from pytesseract import image_to_string


conn = pymysql.connect(host = "localhost",user="root",passwd="",db="no_plate")
myCurser = conn.cursor()
#pytesseract.pytesseract.tesseract_cmd = 'C:\Python27\Lib\site-packages\pytesseract'
x = 'number_plate.jpg'
img=cv2.imread(x)
#decoded_text = text_to_image.decode(x)
#decoded_file_path = text_to_image.decode_to_file(x, "output_text_file.txt")
#img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#bimg=cv2.blur(img,(3,3))
#(image,threshold level,maximum value to be applied,method)
#(T,thresh)=cv2.threshold(img,155,255,cv2.THRESH_BINARY)
#cv2.imshow('out1',thresh2
img1 = Image.open(x)
text=image_to_string(img1, lang = 'eng')
print(text)
text = text.replace(" ","")
text = text.replace("","")
text = text.replace("\n","")
text = text.replace(".","")
print(text)
cv2.waitKey()
cv2.destroyAllWindows()

myCurser.execute("select * from vehical_detail where NO_plate=%s",text)
myresult = myCurser.fetchone()
print(myresult)
print("SQL query fired..!")
conn.commit()
conn.close