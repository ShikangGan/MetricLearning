import math
import numpy as np
import skimage
from skimage import draw
import DPP 
import copy 
Width=600
Height=400

def GridentDescent(polygons):
    learning_rate=2
    center_vectors=DPP.DPP(20,len(polygons))
    for i in range(0,len(center_vectors)):
        if i%2==1:
            center_vectors[i]*=Width
        else:
            center_vectors[i]*=Height
    flag=True
    while flag:
        t=2.0
        flag=False
        c1=copy.copy(center_vectors)
        current_vectors=copy.copy(center_vectors)
        for i in range(0,len(center_vectors)):
            c1[i]+=t
            # a=ObjectiveFunction(tuple(c1),polygons)
            # b=ObjectiveFunction(tuple(center_vectors),polygons)
            # det=(a-b)/t
            det=(ObjectiveFunction(tuple(c1),polygons)-ObjectiveFunction(tuple(center_vectors),polygons))/t 
            center_vectors[i]+=(learning_rate*det)
        print current_vectors
        for i in range(0,len(current_vectors)):
            if abs(current_vectors[i]-center_vectors[i])>=1:
                flag=True
                break
    return current_vectors

def ObjectiveFunction(center_vectors,polygons):
    new_polygons=[]
    for i in range(0,len(center_vectors)/2):
        temp=[]
        for j in range(0,len(polygons[i])):
            if(j%2==0):
                temp.append(polygons[i][j]+center_vectors[2*i])
            else:
                temp.append(polygons[i][j]+center_vectors[2*i+1])
        new_polygons.append(tuple(temp))
    return SumOfDistances(new_polygons)



def SumOfDistances (polygons):
# '''polygons is list of tuples, each tuple represents a polygon'''
    su=float(0)
    for i in range(0,len(polygons)):
        for j in range(i+1,len(polygons)):
            su+=Distance_polygons(polygons[i],polygons[j])
    return su


def Distance_polygons (A,B):
    # A=points[0]
    # B=points[1]
    Ax=A[0::2]
    Ay=A[1::2]
    Bx=B[0::2]
    By=B[1::2]
    Aedge=[]
    Bedge=[]
    dist=[]
    
    for i in range(0,len(Ax)-1):
        Aedge.append(tuple((Ax[i],Ay[i],Ax[i+1],Ay[i+1])))
    Aedge.append(tuple((Ax[-1],Ay[-1],Ax[0],Ay[0])))
    for i in range(0,len(Bx)-1):
        Bedge.append(tuple((Bx[i],By[i],Bx[i+1],By[i+1])))
    Bedge.append(tuple((Bx[-1],By[-1],Bx[0],By[0])))
    # print Aedge,Bedge
    for i in range(0,len(Ax)):
        for j in range(0,len(Bedge)):
            dist.append(Distance_Point2LineSeg(Bedge[j],Ax[i],Ay[i]))
    for i in range(0,len(Bx)):
        for j in range(0,len(Aedge)):
            dist.append(Distance_Point2LineSeg(Aedge[j],Bx[i],By[i]))

    if isPolygonsOverlap(A,B):
        return (-1)*min(dist)
    else:
        return min(dist)

def isPolygonsOverlap(A,B):

    Ax=np.asarray(A[0::2])
    Ay=np.asarray(A[1::2])
    Bx=np.asarray(B[0::2])
    By=np.asarray(B[1::2])

    x1,y1=skimage.draw.polygon(Ax,Ay)
    x2,y2=skimage.draw.polygon(Bx,By)

    x=max(max(x1),max(x2))+1
    y=max(max(y1),max(y2))+1
    
    test=np.zeros((x,y),dtype=int)

    test[x1,y1] +=1
    test[x2,y2] +=1

    for i in range(0,x):
        for j in range(0,y):
            if test[i][j]==2:
                return True
    return False
    



def Distance_Point2LineSeg (edge, x3,y3): # x3,y3 is the point
    x1=edge[0]
    y1=edge[1]
    x2=edge[2]
    y2=edge[3]
    px = x2-x1
    py = y2-y1
    something = px*px + py*py
    u =  ((x3 - x1) * px + (y3 - y1) * py) / float(something)
    if u > 1:
        u = 1
    elif u < 0:
        u = 0
    x = x1 + u * px
    y = y1 + u * py
    dx = x - x3
    dy = y - y3
    # Note: If the actual distance does not matter,
    # if you only want to compare what this function
    # returns to other results of this function, you
    # can just return the squared distance instead
    # (i.e. remove the sqrt) to gain a little performance
    dist = math.sqrt(dx*dx + dy*dy)
    return dist   
GridentDescent(((0,0,130,0,0,150),(60,0,0,120,-60,0,-30,0,-30,-60,30,-60,30,0),(60,0,0,50,-60,0,-30,-40,30,-40)))
print 'finish'
