# -*- coding: utf-8 -*-



import cv2
import numpy as np
import matplotlib



#code to extract text segments from an image
#can seperate different color of page within same page


## to use final function use-
## text_boxes=extract_text(img)
## diag=cyclic_to_diag()
## see bottom

def display(img):
    cv2.imshow("output",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows() 

def load_image(filename):
    img=cv2.imread(filename,0)
    return img

def subimage_diag(img,coord):
    imga=img[coord[0][1]:coord[1][1],coord[0][0]:coord[1][0]]
    return imga

def subimage_cyclic(img,coord):
    imga=img[coord[1][1]:coord[2][1],coord[0][0]:coord[1][0]]    
    return imga
    
    #to cut out sharp lines    
def medianblur(values,ksize):
    median_val=[]
    n=len(values)
    for i in range(n):
        if(i<ksize):
            median_val.append(values[i])
            continue
        if (i+ksize>=n):
            median_val.append(values[i])
            continue
        mdn=np.median(values[i-ksize:i+ksize])
        median_val.append(mdn)
    return median_val

def meanblur(values,ksize):
    mean_val=[]
    n=len(values)
    for i in range(n):
        if(i<ksize):
            mean_val.append(values[i])
            continue
        if (i+ksize>=n):
            mean_val.append(values[i])
            continue
        mdn=np.mean(values[i-ksize:i+ksize])
        mean_val.append(mdn)
    return mean_val
        
    
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

def diag_to_cyclic(coords):
    new=[]
    for i in coords:
        a=i[0]
        b=[i[1][0],i[0][1]]
        d=[i[0][0],i[1][1]]
        c=i[1]
        new.append([a,b,c,d])
    new=np.array(new)
    return new
        
def draw_poly(img,polygon):
    #in cyclic order
    n=len(polygon)
    for i in range(n):
        cv2.line(img,(polygon[i%n][0],polygon[i%n][1]),(polygon[(i+1)%n][0],polygon[(i+1)%n][1]),(10,30,80),1)
        
def histogram(img_0,axis=1,normalize=0,percentil=30,mark=0):
    #axis-1 add all in a row
    #axis-0 add all in a coloumn
    #if mark==1:
    #display(img_0)
    img=img_0.copy()
    try:
        n=len(img)
        m=len(img[0])
    except:
        m=0
        n=0
    #print(n,m)
    values=[]
    if(axis==0):
        values=np.sum(img,axis=axis)/m
        values=255-values
    if(axis==1):
        values=np.sum(img,axis=axis)/n
        values=255-values
        #print (i,') ',val)
    mean_val=np.mean(values)
    min_val=np.percentile(values,percentil)
    #print (values)      
    if normalize==1:
        values=values-min_val
               
    if normalize==2:
        values=values-mean_val
        
    if normalize==1 and axis==0:
        maxi=np.percentile(values,90)
        values=values*20/maxi  
    for i in range(len(values)):
        values[i]=max(values[i],0)
    #print (values)
    if (axis==1 and mark==1):
        for i in range(n):    
            cv2.line(img,(0,i),(max(int(values[i]),0),i),(10,30,80),1)
    if (axis==0 and mark==1):
        for i in range(m):    
            cv2.line(img,(i,0),(i,max(int(values[i]),0)),(10,30,80),1)
    return img,values


#do find colour change region 
def partition(val,img,window=60,threshp=0.15,thresh=5,min_band=50):
    
    #window=min(len(img/4),min_band)
    min_band=max(min_band,len(img)*0.05)
    partitions=[]
    n=len(img)
    m=len(img[0])
    if n<window:
        return partitions
    i=window
    #print(i,n,m)
    while(i<n-window):
        #if i<350:
        #    print (i,val[i],val[i-1],abs(val[i]-val[i-1])/max(val[i],val[i-1],0.01))
        span=5
        if abs(val[min(i+span,n-1-window)]-val[i-1])>thresh or abs(val[min(i+span,n-1-window)]-val[i-1])/max(val[i],val[i-1],0.01)>threshp:
            avg1=sum(val[i-window:i])/window
            avg2=sum(val[i:i+window])/window
            #print (">>>",i,val[i],val[i-1],avg1,avg2,abs(val[i]-val[i-1])/max(val[i],val[i-1],0.01),abs(avg1-avg2)/max(avg1,avg2,0.01))
            if abs(avg1-avg2)>thresh or abs(avg1-avg2)/max(avg1,avg2,0.01)>threshp:
                partitions.append(i)
                #print (">",i,val[i],val[i-1],avg1,avg2,abs(val[i]-val[i-1])/max(val[i],val[i-1],0.01),abs(avg1-avg2))
                #cv2.line(img,(0,i),(m,i),(10,30,80),5)
                i=i+window
                #print ("Done ",i)
        avg=sum(val[i-window:i])/window
        i=i+1
    return partitions



#to find the rows with text /y-coord
def text_partition(val,img,window=2,min_size=3,thresh=3,threshp=0.15,padding=5,draw=0):
    i=window
    partitions=[]
    n=len(img)
    m=len(img[0])
    bandsize=0
    cutoff=7
    low=0
    high=0
    #n=500
    if n<window:
        return partitions
    while(i<n-window):
        avg1=sum(val[i-window:i])/window
        avg2=sum(val[i:i+window])/window
        
        if (avg2-avg1)>thresh or (avg2-avg1)/max(avg1,avg2,0.01)>threshp:
            #print ("enter",i,avg1,avg2)
            #cv2.line(img,(0,i),(m,i),(10,30,80),1)
            low=i
            i=i+2
            while((val[i]>thresh/2 or cutoff>0) and i+window<n):
                if (val[i]<thresh/2):
                    cutoff=cutoff-1
                    #print (i,val[i],"cut=",cutoff)
                    i=i+1
                    continue
                
                bandsize=bandsize+1
                #print (i,val[i],"band=",bandsize)
                i=i+1
            
            high=i
            if bandsize>min_size :
                low=max(low-padding,0)
                high=min(high+int(padding/2),n)
                partitions.append((low,high))
                
                #print("Entering ",low,high)
                if(draw==1):
                    cv2.line(img,(0,low),(m,low),(0,0,0),1)
                    cv2.line(img,(0,high),(m,high),(127,127,127),1)
        bandsize=0
        cutoff=5
        i=i+1
    return partitions


def text_in_line(img,val,smoothen=2,thresh=3,min_band=20,max_gap=25,padding=2):
    text=[(0,0)]
    n=len(img)
    m=len(img[0])
    l=len(val)
    #print(n,m,l)
    val=meanblur(val,smoothen)
    band=0
    low=0
    high=0
    cutoff=max_gap
    i=0
    #l=300
    while (i<l-1):
        #print ("values are",i,val[i])
        if val[i]>3*thresh and i<l-1 :
            low=i
            #print("starting at ",i)
            while( (val[i]>thresh or cutoff>0) and i<l-1):
                #print (">>values are",i,val[i],cutoff,low)
                #print (i)
                if val[i]<thresh:
                    cutoff=cutoff-1
                    i=i+1
                    continue
                band=band+1
                cutoff=min(cutoff+0.5,max_gap)
                i=i+1
            if band>min_band or i==l-2:
                high=min(i+padding,m)
                low=max(0,low-padding)
                last=text[-1]
                if (abs(low-last[1])<2*max_gap):
                    last=text.pop()
                    text.append((last[0],high))
                else:
                    text.append((low,high))
                #print(low,high)
            else:
                i=low+2
            band=0
            cutoff=max_gap
        i=i+1
#    for i in text:
#        cv2.line(img,(i[0],0),(i[0],int(n/2)),(0,0,0),1)
#        cv2.line(img,(i[1],int(n/2)),(i[1],n),(10,30,80),1)
        
    #print ("texts-",text)
    #display(img)
    return text


def text_box(img,low):
    #to find both x-coords and y-coords of text lines
    
    img1,values=histogram(img,normalize=1,mark=1)
    #display(img1)
    box_coord=[]
    #print("Partitioning") 
    #display(img)
    txt_prt=text_partition(values,img)   ## to find lines of text
    #display(img)
    #print("Finding x-limits")
    for i in txt_prt:    #find text in each line
        #print ("Working on line",i)
        img1,values=histogram(img[i[0]:i[1]],axis=0,normalize=1,percentil=30)
        #print(len(values),values[:5])
        text=text_in_line(img,val=values,smoothen=2,thresh=2,min_band=20,max_gap=25,padding=2)
        for j in text:
            coord=[[j[0],low+i[0]],[j[1],low+i[0]],[j[1],low+i[1]],[j[0],low+i[1]]]   #order chaged (x,y)
            box_coord.append(coord)
        #display(img1)
    return box_coord
 
    
#to find all text rows/lines ycoord
def detect_text(img,parts,buffer=0):
    low=0
    box_coords=[]    
    for i in range(len(parts)):
#    for i in range(1):
        high=min(parts[i]+buffer,len(img))
        box_coord=text_box(img[low:high],low)
        box_coords=(box_coords+box_coord)
        #print("text for image",i,box_coord)
        #box_coord.append(coord)
        low=max(0,parts[i]-buffer)        
    high=len(img)
    box_coord=text_box(img[low:high],low)
    #print("text for image",i+1,box_coord)
    box_coords=(box_coords+box_coord)
    #print ("Final:",box_coords)
    return box_coords

def extract_text(img):
    img1=img[:,:30]
    img2=img[:,-60:]
    #img1=img1+img2
    img1=np.concatenate((img1,img2),axis=1)
    img1,values=histogram(img1)
    #display(img)
    mval=medianblur(values,4)
    parts=partition(mval,img)
    #parts=[]
    #print ("parts",parts)
    #cv2.imwrite("output.jpeg",img)
    img1=img.copy()
    #img1 = cv2.imread('2.png', 0)
    #img1=img
    text_boxes=detect_text(img1,parts)
    text_box_filtered=[]
    for i in text_boxes:
        if i[0][0]!=i[1][0] and i[1][1]!=i[2][1]:
            text_box_filtered.append(i)
    return text_box_filtered

#imagename="doc.jpeg"
#imagename="hr.jpg"
#imagename="doc2.jpg"
#imagename="medical7.jpg"
#imagename="2.png"
#img = cv2.imread(imagename, 0)
        
 
#text_boxes=extract_text(img)
#diag=cyclic_to_diag(text_boxes)

### to display and save output
#for i in text_boxes:
#    draw_poly(img,i)
#cv2.imwrite("output1.jpeg",img)
#display(img)

# 271 242.927777778 242.927777778 245.182444444 232.505444444 0.0 0.0517043543991
#271 244.135 244.135 0.0
#271 242.927777778 242.927777778 0.0
