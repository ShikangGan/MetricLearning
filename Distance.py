import math

def Distance_polygons(points):
    A=points[0]
    B=points[1]
    Ax=A[0::2]
    Ay=A[1::2]
    Bx=B[0::2]
    By=B[1::2]
    Aedge=[]
    Bedge=[]
    for i in range(0,Ax.length()-1):
        Aedge+=(Ax[i],Ay[i],Ax[i+1],Ay[i+1])
    Aedge+=(Ax[-1],Ay[-1],Ax[0],Ay[0])
    for i in range(0,Bx.length()-1):
        Bedge+=(Bx[i],By[i],Bx[i+1],By[i+1])
    Bedge+=(Bx[-1],By[-1],Bx[0],By[0])

def Distance_Point2LineSeg (x1,y1, x2,y2, x3,y3): # x3,y3 is the point
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
