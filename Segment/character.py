# -*- coding: utf-8 -*-


from textbounds import *
from draw import *
#from smart_ocr import *
import cv2
import sys
import os
#imagename="doc.jpeg"
#img = cv2.imread(imagename, 0)

def segement(img):
    
    text_boxes=extract_text(img)
    diag=cyclic_to_diag(text_boxes)
    img2=drawdottedbox(img,diag)
    
    
    text_boxes,diag=get_lines(img,diag)
    img3=drawdottedbox(img,diag)
    
    
    text_boxes,diag=get_wordbox(img,text_boxes,handpart=[0,4000])
    img4=drawdottedbox(img,diag)
    #display(img2)
    #display(img3)
    #display(img4)
    cv2.imwrite("original.jpg",img)
    cv2.imwrite("stage1.jpg",img2)
    cv2.imwrite("stage2.jpg",img3)
    cv2.imwrite("segmentedoutput.jpg",img4)
    return img,diag

def divide_line(img,c):
    imga=subimage_diag(img,c)
    #display(imga)
    #cv2.imwrite("sublineo1.jpg",imga)
    imgb,values=histogram(imga,axis=1,normalize=1,percentil=30,mark=1)
    #display(imgb)
    #cv2.imwrite("subline1.jpg",imgb)
    #txt_prt=text_partition(values,imgb,draw=1)
    text=text_in_line(imga,val=values,smoothen=1,thresh=3,min_band=5,max_gap=2,padding=5)
    
    new_lines=[]
    for t in text:
        low=t[0]
        high=t[1]
        m=len(imgb[0])
        cv2.line(imgb,(0,low),(m,low),(0,0,0),1)
        cv2.line(imgb,(0,high),(m,high),(127,127,127),1)
    
        lx=c[0][0]
        hx=c[1][0]
        ly=t[0]+c[0][1]
        hy=t[1]+c[0][1]
        coord=[[lx,ly],[hx,hy]]
        #print ('>>',coord)
        if (lx!=hx and ly!=hy):
            new_lines.append(coord)
    #display(imgb)
    return new_lines
    
def wordbox_from_textbox(img,coord):
    i=coord
    imga=subimage_diag(img,i)
    print (i)
    #display(imga)
    #cv2.imwrite('Case-B/word.jpg',imga)
    imgb,values=histogram(imga,axis=0,normalize=1,percentil=30,mark=1)
    #display(imgb)
    #cv2.imwrite('Case-B/wordhist.jpg',imgb)
    text=text_in_line(imga,val=values,smoothen=2,thresh=2,min_band=10,max_gap=5,padding=2)
    buf=10
    text=np.array(text)
    coords=[]
    for j in text:
        j[0]=max(0,j[0]-buf)
        j[1]=min(len(imga[0]),j[1]+buf)
        
        pt1=[j[0]+i[0][0],i[0][1]]
        pt2=[j[1]+i[0][0],i[1][1]]
        coord=[pt1,pt2]
        coords.append(coord)
    return coords

def get_wordbox(img_0,text_boxes,handpart=[0,4000]):
    handpart[1]=min(handpart[1],len(img_0))
    img=img_0.copy()
    new_box=[]
    text_boxes=np.array(text_boxes)
    diag=cyclic_to_diag(text_boxes)
    new_diag=[]
    for k in range(len(diag)):
        i=diag[k]
        if i[0][1]<handpart[0] or i[1][1]>handpart[1]:
            new_diag.append(i)
        else:
            words=wordbox_from_textbox(img,i)
            for j in words:
                new_diag.append(j)
    new_box=diag_to_cyclic(new_diag)
    return new_box,new_diag
    

def get_lines(img_0,diag,handpart=[0,4000]):
    handpart[1]=min(handpart[1],len(img_0))
    img=img_0.copy()
    new_box=[]
    
    diag=np.array(diag)
    new_diag=[]
    for k in range(len(diag)):
        i=diag[k]
        if i[0][1]<handpart[0] or i[1][1]>handpart[1]:
            new_diag.append(i)
        else:
            lines=divide_line(img,i)
            for j in lines:
                new_diag.append(j)
                #display(drawdottedbox(img,new_diag))
    new_box=diag_to_cyclic(new_diag)
    return new_box,new_diag




#img=load_image("doc.jpeg")
#run(img)




#for i in diag:
#    imga=subimage_diag(img,i)
#    #display(imga)
#    imgb=imga.copy()
#    imgb,values=histogram(imga,axis=0,normalize=1,percentil=30,mark=1)
#    #imgb,values=histogram(imgb,axis=1,normalize=1,percentil=30,mark=1)
#    text=text_in_line(imga,val=values,smoothen=2,thresh=2,min_band=10,max_gap=5,padding=2)
#    t=''
#    
#    for j in text:
#        j[0]=max(0,j[0]-buf)
#        j[1]=min(len(imga[0]),j[1]+buf)
#        
#        pt1=[j[0]+i[0][0],i[0][1]]
#        pt2=[j[1]+i[0][0],i[1][1]]
#        coord=[pt1,pt2]
#        drawrect(img,pt1,pt2,(0,0,0),thickness=1,style='dotted')
    
#display(img)
#cv2.imwrite('words.jpg',img)
    #display(imgb)
    
