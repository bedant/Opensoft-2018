# -*- coding: utf-8 -*-

import pytesseract
from PIL import Image
import numpy as np
from textbounds import *
from character import *
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'

def convt_to_text(img):
    t=pytesseract.image_to_string(img)
    return t

def drawtext(img2,img1,t,coord):  #write in output page
    print (t)
    #display(img1)
    color=min(np.mean(img1)+5,255)
    font= cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (int((coord[2]+coord[2])/2),int((coord[0]+coord[1])/2))
    fontScale= 0.6
    if color<150:
        fontColor= (255,255,255)
    if color>=150:
        fontColor=(0,0,0)
    lineType= 1
    
    #cv2.rectangle(img,(coord[3],coord[1]),(coord[2],coord[0]),(color,color,color),-1)
    #cv2.rectangle(img2,(coord[3],coord[1]),(coord[2],coord[0]),(fontColor),1)
    cv2.putText(img2,t,bottomLeftCornerOfText,font,fontScale,fontColor,lineType)
    

def smart_text_conv1(img,diag):
    x=5
    images=[]
    m=len(img)
    n=len(img[0])
    text=''
    img2 = np.ones((m,n), np.uint8)*255
    j=0
    for i in diag:
        j=j+1
        lx=max(i[0][1]-x,0)
        hx=min(i[1][1]+x,m)
        ly=max(i[0][0]-x,0)
        hy=min(i[1][0]+x,n)
        if(lx!=hx and ly!=hy):
            #print(lx,hx,ly,hy)
            img1=(img[lx:hx,ly:hy])  #subimage inside box
            coords=[lx,hx,ly,hy]
            t=(pytesseract.image_to_string(img1)) #read text in box
            text=text+'\n'+t
            #drawrect(img2,[ly,lx],[hy,hx],(0,0,0))
            drawtext(img2,img1,t,coords)
        print (int(j*100/len(diag)),'% completed')
    #display(img2)
    return img2,text

def read_page1(img,diag):
    #display(img)
    text=''
    #text_boxes=extract_text(img)
    #print(text_boxes)
    #diag=cyclic_to_diag(text_boxes)
    #print (diag)
    img2,text=smart_text_conv1(img,diag)
    cv2.imwrite("textoutput.jpg",img2)
    return img2,text,img

#img2,text=read_page(img)
#display(img2)
#cv2.imwrite("output1.jpeg",img2)
    
    
