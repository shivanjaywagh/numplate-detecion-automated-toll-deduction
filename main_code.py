import cv2
import numpy as np
import  imutils
import pymysql
from PIL import Image
from pytesseract import image_to_string
import re

#connecting to database
conn = pymysql.connect(host = "localhost",user="root",passwd="",db="no_plate")
myCurser = conn.cursor()

#resizing the image
img_org = cv2.imread('car5.jpg')
size = np.shape(img_org)
if size[0] <= 776:
    img_org = imutils.resize(img_org , 900)

#thresholding the image
img_org2 = img_org.copy()
img_bw = cv2.cvtColor(img_org , cv2.COLOR_BGR2GRAY)
ret3,img_thr = cv2.threshold(img_bw,125,255,cv2.THRESH_BINARY)
cv2.imwrite('thresh.jpg',img_thr)

#Canny's Edge Detection
img_edg  = cv2.Canny(img_thr ,100,200)
cv2.imwrite('cn_edge.jpg' , img_edg)

#increasing the thickness of the edges
kernel = cv2.getStructuringElement(cv2.MORPH_DILATE, (7, 7))
img_dil = cv2.dilate(img_edg, kernel, iterations = 1)

cv2.imwrite('dilated_img.jpg',img_dil)

#finding the contours and sorting them in descending order
(contours ,hierarchye) = cv2.findContours(img_dil.copy(), 1, 2)
cnts = sorted(contours, key = cv2.contourArea, reverse = True)[:10]

#giving shape to the contours
screenCnt = None	 

for c in cnts:
	# approximate the contour 
	peri = cv2.arcLength(c, True) #true=closed contour
	approx = cv2.approxPolyDP(c, 0.02 * peri, True)#approx PolyDP shapes it approximately to a nearby image size

	# if our approximated contour has four points, then
	# we can assume that we have found our screen
	if len(approx) == 4:
		screenCnt = approx
		break

#drawing contour around number plate
mask = np.zeros(img_bw.shape, dtype=np.uint8)
roi_corners = np.array(screenCnt ,dtype=np.int32)
ignore_mask_color = (255,)*1
cv2.fillPoly(mask, roi_corners , ignore_mask_color)
cv2.drawContours(img_org, [screenCnt], -40, (100, 255, 100), 9)
cv2.imshow('original  image with boundry' , img_org)
cv2.imwrite('plate_detedted.jpg',img_org)

ys =[screenCnt[0,0,1] , screenCnt[1,0,1] ,screenCnt[2,0,1] ,screenCnt[3,0,1]]
xs =[screenCnt[0,0,0] , screenCnt[1,0,0] ,screenCnt[2,0,0] ,screenCnt[3,0,0]]

ys_sorted_index = np.argsort(ys)
xs_sorted_index = np.argsort(xs)

x1 = screenCnt[xs_sorted_index[0],0,0]
x2 = screenCnt[xs_sorted_index[3],0,0]

y1 = screenCnt[ys_sorted_index[0],0,1]
y2 = screenCnt[ys_sorted_index[3],0,1]

img_plate = img_org2[y1:y2 , x1:x2]
# for i in screenCnt:
#     print(i)
# print xs , ys
# print x1,x2,y1,y2
cv2.imshow('number plate',img_plate)
cv2.imwrite('number_plate.jpg',img_plate)
cv2.waitKey(0)

#converting the image content to text
x = 'number_plate.jpg'
img=cv2.imread(x)

img1 = Image.open(x)
text=image_to_string(img1, lang = 'eng')
print(text)
text = " ".join(re.split("[^a-zA-Z0-9]*",text))
text = text.replace(" ","")
text = text.replace("\n","")
text = text.replace("~","")
text = text.replace(".","")
print(text)
cv2.waitKey()
cv2.destroyAllWindows()
myCurser.execute("select addhar_no from vehical_detail where NO_plate=%s",text)
myresult = myCurser.fetchone()
if myresult == None:
	print("Suspicious number plate detected!!!")
myCurser.execute("select account_no from bank_addhar_detail where addhar_no=%s",myresult)
bankaccount = myCurser.fetchone()
myCurser.execute("select amount from bank_addhar_detail where account_no=%s",bankaccount)
balance = myCurser.fetchone()
print(balance)
print("---------------------------------------------------------------------------------------")
print ("Detected Number : ")
print(text)

k = 1000
print("Aadhar number of vehicle owner : ", myresult)
print("Account number of vehicle owner : ",bankaccount)

if(balance > k):
	myCurser.execute("update bank_addhar_detail set amount=amount-100 where account_no=%s",bankaccount)
	myCurser.execute("update toll_detail set amount_t=amount_t+100 where toll_name='PS'")
	print("Transaction successful...!")
else:
	print("Transaction failed...Low balance..!!")

print("---------------------------------------------------------------------------------------")

conn.commit()

conn.close