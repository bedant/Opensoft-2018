# -*- coding: utf-8 -*-


import cv2
import numpy as np

def cyclic_to_diag(coords):
    new=[]
    for i in coords:
        lx=i[0][1]
        hx=i[2][1]
        ly=i[0][0]
        hy=i[1][0]
        a=[[ly,lx],[hy,hx]]
        new.append(a)
    return new


def drawline(img,pt1,pt2,color,thickness=1,style='dotted',gap=10):
    dist =((pt1[0]-pt2[0])**2+(pt1[1]-pt2[1])**2)**.5
    pts= []
    for i in  np.arange(0,dist,gap):
        r=i/dist
        x=int((pt1[0]*(1-r)+pt2[0]*r)+.5)
        y=int((pt1[1]*(1-r)+pt2[1]*r)+.5)
        p = (x,y)
        pts.append(p)

    if style=='dotted':
        for p in pts:
            cv2.circle(img,p,thickness,color,-1)
    else:
        s=pts[0]
        e=pts[0]
        i=0
        for p in pts:
            s=e
            e=p
            if i%2==1:
                cv2.line(img,s,e,color,thickness)
            i+=1

def drawpoly(img,pts,color,thickness=1,style='dotted',):
    s=pts[0]
    e=pts[0]
    pts.append(pts.pop(0))
    for p in pts:
        s=e
        e=p
        drawline(img,s,e,color,thickness,style)

def drawrect(img,pt1,pt2,color,thickness=1,style='dotted'):
    pts = [pt1,(pt2[0],pt1[1]),pt2,(pt1[0],pt2[1])] 
    drawpoly(img,pts,color,thickness,style)
    
def drawdottedbox(img,coords):
    img1=img.copy()
    if len(coords[0])==4:
        coords=cyclic_to_diag(coords)
    for i in coords:
        drawrect(img1,i[0],i[1],(0,0,0),thickness=1,style='dotted')
        
    return img1