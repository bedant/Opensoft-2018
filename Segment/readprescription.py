# -*- coding: utf-8 -*-


from character import *
#from smart_ocr import *



def OCRhand(img,typ):
    
    
    text='OCRhand'
    return text

def OCRtext(img,typ):
    
    
    text='OCRtext'
    return text

def get_type(img,coord):
    m=len(img[0])
    n=len(img)
    lx=coord[2]
    hx=coord[3]
    ly=coord[0]
    hy=coord[1]
    xav=(lx+hx)/2
    yav=(ly+hy)/2
    z =float(yav)/n
    a=float(xav)/m-.03
    if z<.13:
        return ['clinic',1]
    if z<.258:
        return ['doctor',1]
    if z<0.3:
        if a>.19 and a<.52:
            return ['pname',0]
        if a>.57 and a<.76 :
            return ['page',0]
        if a> .80 and a<1 :
            return ['psex',0]
        return 'name'
    if z<.333:
        return ['remarkstext',1]
    if z<.483:
        return ['remarks',0]
    if z<.5:
        
        return ['medicinetext',1]
    if z<.893:
        if a<.63:
            return ['medicinename',0]
        else :
            return ['dose',0]
    return ['contact',1]

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

    

def smart_text_conv(img,diag):
    x=10
    images=[]
    m=len(img)
    n=len(img[0])
    text=''
    data=[]
    img2 = np.ones((m,n), np.uint8)*255
    j=0
    typ='apple'
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
            g=get_type(img,coords)
            #t=(pytesseract.image_to_string(img1)) #read text in box
            
            if (g[1]==1):
                t=OCRtext(img,typ)
            if (g[1]==0):
                t=OCRhand(img,typ)
            t=t+g[0]
            text=text+'\n'+t
            drawtext(img2,img1,t,coords)
            #drawrect(img2,[ly,lx],[hy,hx],(0,0,0))
            
            dia=[[lx,ly],[hx,hy]]
            data.append((typ,dia,t))
        print (int(j*100/len(diag)),'% completed')
    #display(img2)
    return img2,text


def read_page(img,diag):
    #display(img)
    text=''
    #text_boxes=extract_text(img)
    #print(text_boxes)
    #diag=cyclic_to_diag(text_boxes)
    #print (diag)
    img2,text=smart_text_conv(img,diag)
    cv2.imwrite("textoutput.jpg",img2)
    return img2,text,img

def main():
    args=sys.argv[1:]
    filename=args[0]
    img=load_image(filename)
    text_boxes=extract_text(img)
    print('TextBox Extracted')
    diag=cyclic_to_diag(text_boxes)
    try :
        print("attempting deep segementation")
        
        img1,diag1=segement(img)
        print ("deep segementation sucessful")
        print("Applying custom OCR")
        
        img2,text,img=read_page(img,diag)
        
        
    except:
        #print(" Deep segementation failed")
        print("Applying custom OCR")
        
        img2,text,img=read_page(img,diag)
    print("press enter to save and continue")
    display(img2)
    cv2.imwrite('digital_prescription.jpg',img2)
    print("Completed!! File saved as digital_prescription.jpg")

if __name__ == "__main__":
    main()

