

import sys
import re
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import random
from math import *
import numpy as np
import skimage
from skimage import draw
import Distance
import DPP
import time

# --- canvas ---
Width=600
Height=400


#initialize

# learning_rate=1

# function_value=0

Polygons=(
    (60,0,0,120,-60,0,-30,0,-30,-60,30,-60,30,0),
    (30,40,130,0,0,150),
    (60,0,0,50,-60,0,-30,-40,30,-40),    
    (20,20,20,-20,-20,-20,-20,20),
    (50,50,70,120,20,100),
    (30,30,30,-30,-30,-30,-30,30),
    (40,-40,-40,40,-15,80,15,80),
    (40,40,40,-40,-40,-40,-40,40)
)

center_vectors=DPP.DPP(20,len(Polygons))
for i in range(0,len(Polygons)):
    x=list(Polygons[i])[0::2]
    y=list(Polygons[i])[1::2]
    center_vectors[2*i]*=Width
    center_vectors[2*i+1]*=Height
    shift_x=0
    shift_y=0

    if min(x)+center_vectors[2*i]<0:
        shift_x=abs(min(x)+center_vectors[2*i])
    if max(x)+center_vectors[2*i]>Width-1:
        shift_x=Width-1-max(x)-center_vectors[2*i]
    if min(y)+center_vectors[2*i+1]<0:
        shift_y=abs(min(y)+center_vectors[2*i+1])
    if max(y)+center_vectors[2*i+1]>Height-1:
        shift_y=Height-1-max(y)-center_vectors[2*i+1]
    
    center_vectors[2*i]+=shift_x
    center_vectors[2*i+1]+=shift_y

class MyCanvas(QtGui.QWidget):
    
    # shapes=[]
    
    def __init__(self):
        super(MyCanvas, self).__init__()

        # default size
        self.setFixedSize(Width, Height)

        
    def paintEvent(self, event):

        qp = QtGui.QPainter()
        qp.begin(self)

        # white background
        qp.fillRect(event.rect(), QtGui.QBrush(QtGui.QColor('white')))



        for i in range(0,len(Polygons)):
            self.drawPolygonWithCenter(qp,center_vectors[i*2],center_vectors[i*2+1],Polygons[i])
            # print 'item',i

        

        # print "update"

                
        qp.end()
    

    def drawPolygonWithCenter(self,qp,x,y,polygon):
        new_polygon=[]
        for i in range(0,len(polygon)):
            if i%2==0:
                new_polygon.append(polygon[i]+x)
            else:
                new_polygon.append(polygon[i]+y)
        self.drawPolygon(qp,*tuple(new_polygon))

        
    def drawPolygon(self, qp, *points):     
        '''drawing polygon'''

        #set color                  
        # qp.setBrush(QtGui.QColor('gold'))

        temp_list=[]
        # # create polygon
        num=points.__len__()/2
        for i in range(0,num):
            temp_list.append(QPoint(points[2*i],points[2*i+1]))        

        # draw
        qp.drawConvexPolygon(QPolygon(temp_list))
        






class App(QtGui.QWidget):

    def __init__(self):
        super(App, self).__init__()
        self.learning_rate=[2]*len(center_vectors)
        self.function_value=0

        self.initUI()
    def restart(self):  

        

        a=Distance.GridentDescent(center_vectors,Polygons,self.learning_rate,self.function_value)
        self.canvas.update()
        # self.function_value=a
        # print 'final',center_vectors,'\n'*3,'value',self.function_value,'\t','rate',self.learning_rate,'\n'*3,
        
        return a
    
    def test(self):
        for i in range(0,15):
            self.restart()
            # print i
        


    def initUI(self):      

        self.vbox = QtGui.QVBoxLayout(self)
        self.setLayout(self.vbox)

        #--- canvas - created to get tool list ---
        
        self.canvas = MyCanvas() 

        
        self.restart()
        # self.test()
            
               

        self.btn=QPushButton("next step")
        self.btn.setCheckable(True)
        self.btn.setAutoExclusive(True)
        self.btn.clicked.connect(self.restart)

        self.btn1=QPushButton("finish all steps")
        self.btn1.setCheckable(True)
        self.btn1.setAutoExclusive(True)
        self.btn1.clicked.connect(self.test)

         #--- canvas - add to window ---
        self.vbox.addWidget(self.canvas)
        self.vbox.addWidget(self.btn)
        self.vbox.addWidget(self.btn1)
       
        
        #self.setGeometry(300, 300, 600, 170)
        self.setWindowTitle('MyCanvas')
        self.show()

        

        
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
