import math
import numpy as np
import skimage
from skimage import draw
import DPP 
import LineIntersection
import copy 
Width=600
Height=400
import time

total_time = [1]

def GridentDescent(center_vectors,polygons,learning_rate,value):

    flag=True
    while flag:
        t=0.5
        flag=False

        current_vectors=copy.copy(center_vectors)
        
        
        for i in range(0,len(center_vectors)):
            
            c1=copy.copy(center_vectors)
            c1[i]+=t


            det=(ObjectiveFunction(tuple(c1),polygons)-ObjectiveFunction(tuple(center_vectors),polygons))/t 



            # center_vectors[i]+=(learning_rate[i]*det)
            # center_vectors[i]=int(center_vectors[i]-(learning_rate*det))

            if det>0:
                # learning_rate[i]*=1.5
                center_vectors[i]+=(learning_rate[i]*det)                
            else:
                # learning_rate[i]*=0.8
                center_vectors[i]+=(learning_rate[i]*det) 
                # if learning_rate[i]<0.001:
                #     learning_rate[i]=1   

            if isPolygonOutOfBound(center_vectors[i/2*2],center_vectors[i/2*2+1],polygons[i/2]):
                center_vectors[i]=current_vectors[i]
                # learning_rate[i]=0.01

    
        return ObjectiveFunction(tuple(center_vectors),polygons)





def isPolygonOutOfBound(x,y,polygon):
    for i in range(0,len(polygon)):
        if i%2==0:
            a=polygon[i]+x
            if a<0 or a>Width:
                return True
        else:
            a=polygon[i]+y
            if a<0 or a>Height:
                return True
    return False


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
    
    # return SumOfDistances(new_polygons)+0.5*MinOfDistances(new_polygons)

   
    result = test(new_polygons)
    return result



def SumOfDistances (polygons):
# '''polygons is list of tuples, each tuple represents a polygon'''
    su=float(0)
    for i in range(0,len(polygons)):
        for j in range(i+1,len(polygons)):
            su+=Distance_polygons(polygons[i],polygons[j],True)
    return su
def MinOfDistances(polygons):
    temp=[]
    for i in range(0,len(polygons)):
        for j in range(i+1,len(polygons)):
            temp.append(Distance_polygons(polygons[i],polygons[j],False))
    return min(temp)
def ProdOfDistance(polygons):
    po=float(1)
    for i in range(0,len(polygons)):
        for j in range(i+1,len(polygons)):
            po*=Distance_polygons(polygons[i],polygons[j],True)
    return po

def test(polygons):
    mi=0.0
    su=0.0
    for i in range(0,len(polygons)):
        temp=[]
        for j in range(0,len(polygons)):
            if i!=j:
                temp.append(Distance_polygons(polygons[i],polygons[j],True))
        mi+=min(temp)
        su+=sum(temp)
    return mi+su/len(polygons)/2


def Distance_polygons (A,B,flag):
    #flag False means do not consider the overlap problem

    Ax=A[0::2]
    Ay=A[1::2]
    Bx=B[0::2]
    By=B[1::2]
    Aedge=[]
    Bedge=[]
    dist=[]
    

    l1 = time.time()
   


    for i in range(0,len(Ax)-1):
        Aedge.append(tuple((Ax[i],Ay[i],Ax[i+1],Ay[i+1])))
    Aedge.append(tuple((Ax[-1],Ay[-1],Ax[0],Ay[0])))
    for i in range(0,len(Bx)-1):
        Bedge.append(tuple((Bx[i],By[i],Bx[i+1],By[i+1])))
    Bedge.append(tuple((Bx[-1],By[-1],Bx[0],By[0])))
    l2 = time.time()
    
    # print Aedge,Bedge
    for i in range(0,len(Ax)):
        for j in range(0,len(Bedge)):
            dist.append(Distance_Point2LineSeg(Bedge[j],Ax[i],Ay[i]))
    for i in range(0,len(Bx)):
        for j in range(0,len(Aedge)):
            dist.append(Distance_Point2LineSeg(Aedge[j],Bx[i],By[i]))
    
    if flag:
        if isPolygonsOverlap(A,B):
            return (-1)*(min(dist))*20
        else:
            return min(dist)
    else:
        return min(dist)




def isPolygonsOverlap(A,B):

    # return True means overlap

    Ax=A[0::2]
    Ay=A[1::2]
    Bx=B[0::2]
    By=B[1::2]
    Aedge=[]
    Bedge=[]
    
    for i in range(0,len(Ax)-1):
        Aedge.append(tuple((Ax[i],Ay[i],Ax[i+1],Ay[i+1])))
    Aedge.append(tuple((Ax[-1],Ay[-1],Ax[0],Ay[0])))
    for i in range(0,len(Bx)-1):
        Bedge.append(tuple((Bx[i],By[i],Bx[i+1],By[i+1])))
    Bedge.append(tuple((Bx[-1],By[-1],Bx[0],By[0])))

    for i in range(0,len(Aedge)):
        for j in range(0,len(Bedge)):
            if LineIntersection.IfLineIntersect(Aedge[i],Bedge[j]):
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

    dist = math.sqrt(dx*dx + dy*dy)
    return dist

