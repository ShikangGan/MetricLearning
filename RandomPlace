#!/usr/bin/env python3

# http://zetcode.com/gui/pyqt4/drawing/
# https://pl.python.org/forum/index.php?topic=6010.msg25683#msg25683

# maybe better to use QGraphicsView, QGraphicsScene, QGraphicsItem

import sys
import re
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import random
from math import *
import numpy as np
# --- canvas ---
Width=600
Height=400
pixelmat=np.zeros((Width,Height))
shapes=[]
ShapeBase=[
    ('Circle',60), # radius
    ('Ellipse',50,140), # radius in x,y
    ('Ellipse',100,40),
    ('Rectangle',80,40),
    ('Polygon',20,0,0,40,-20,0,-10,0,-10,-20,10,-20,10,0),
    ('Triangle',0,0,130,0,0,150),
    ('Polygon',60,0,0,50,-60,0,-30,-40,30,-40)
]
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



        # drawing shapes from list
        for shape in shapes:
            if shape[0] == 'circle':
                self.drawCircle(qp,shape[1],shape[2],shape[3])
            elif shape[0] == 'ellipse':
                self.drawEllipse(qp,shape[1],shape[2],shape[3],shape[4],shape[5])
            elif shape[0] == 'rectangle':
                self.drawRect(qp,shape[1],shape[2],shape[3],shape[4])
            elif shape[0] == 'polygon':
                self.drawPolygon(qp,*shape[1])




                
        qp.end()
    
    def CircleGenerator(self,centerX,centerY,radius):

        flag=True
        exit_flag=False
        x1=centerX-radius
        x2=centerX+radius
        y1=centerY-radius
        y2=centerY+radius
        if(x1<0 or x2>=Width or y1<0 or y2>=Height):
            flag=False
        else:
            for i in range(x1,x2+1):
                for j in range(y1,y2+1):
                    if ((i-centerX)**2+(j-centerY)**2) <= (radius**2) and pixelmat[i,j]!=0 :
                        flag=False
                        exit_flag=True
                        break
                if(exit_flag==True):
                    break
        if(flag==True):
            for i in range(x1,x2+1):
                for j in range(y1,y2+1):
                    if ((i-centerX)**2+(j-centerY)**2) <= (radius**2):
                        pixelmat[i,j]=1
            shapes.append(('circle',centerX,centerY,radius))
            self.update()
            # self.DrawPicture()
            return True
        else:
            self.ErrorMessage()
            return False

    def EllipseGenerator(self,centerX,centerY,radiusX,radiusY,angle=0):
        # angle=angle/180.0*pi
        co=cos(angle/180.0*pi)
        si=sin(angle/180.0*pi)
        if radiusX>=radiusY:
            r=radiusX
        else:
            r=radiusY
        flag=True
        exit_flag=False
        for i in range(centerX-r,centerX+r-1):
            for j in range(centerY-r,centerY+r-1):
                if (((i-centerX)*co+(j-centerY)*si)**2/(radiusX**2)+(-(i-centerX)*si+(j-centerY)*co)**2/(radiusY**2)) <=1:
                    if i<0 or i>=Width or j<0 or j>=Height:
                        flag=False
                        exit_flag=True
                        break
                    elif pixelmat[i,j]!=0:
                        flag=False
                        exit_flag=True
                        break
            if(exit_flag==True):
                break
        if(flag==True):
            for i in range(centerX-r,centerX+r-1):
                for j in range(centerY-r,centerY+r-1):
                    if (((i-centerX)*co+(j-centerY)*si)**2/(radiusX**2)+(-(i-centerX)*si+(j-centerY)*co)**2/(radiusY**2)) <=1:
                    # if (i*cos(angle)+j*sin(angle)-centerX)**2.0/(radiusX**2)+(-i*sin(angle)+j*cos(angle)-centerY)**2/(radiusY**2)<=1:
                        pixelmat[i,j]=1
          
            shapes.append(('ellipse',centerX,centerY,radiusX,radiusY,angle))
            self.update()
            return True
        else:
            self.ErrorMessage()
            return False

    def RectangleGenerator(self,centerX,centerY,width,height):
        flag=True
        exit_flag=False
        for i in range(centerX-width/2,centerX+width/2):
            for j in range(centerY-height/2,centerY+height/2):
                if pixelmat[i,j]!=0:
                    flag=False
                    exit_flag=True
                    break
            if(exit_flag==True):
                break
        if(flag==True):            
            for i in range(centerX-width/2,centerX+width/2):
                for j in range(centerY-height/2,centerY+height/2):
                    pixelmat[i,j]=1
            
            shapes.append(('rectangle',centerX,centerY,width,height))
            self.update()
            return True
        
        else:
            self.ErrorMessage()
            return False

    def PolygonGenerator(self,*points):
        flag=True
        exit_flag=False
        x1=min(points[0::2])
        x2=max(points[0::2])
        y1=min(points[1::2])
        y2=max(points[1::2])
        num=points.__len__()
        if x1<0 or x2>=Width or y1<0 or y2>=Height:
            flag=False
        else:
            for i in range(x1,x2):
                for j in range(y1,y2):
                    if self.ifInPolygon(i,j,*points):
                        if pixelmat[i,j]!=0:
                            flag=False 
                            exit_flag=True
                            break
                if(exit_flag==True):
                    break
        if(flag==True):
            for i in range(x1,x2):
                for j in range(y1,y2):
                    if self.ifInPolygon(i,j,*points):
                        pixelmat[i,j]=1
            shapes.append(('polygon',points))
            self.update()
            return True
        else:
            self.ErrorMessage()
            return False

    def ifInPolygon(self,x,y,*points):
        sum_degree=0
        num=points.__len__()/2
        for i in range(0,num-1):
            sum_degree+=self.get_degree(x,y,points[2*i],points[2*i+1],points[2*i+2],points[2*i+3])
        sum_degree+=self.get_degree(x,y,points[0],points[1],points[-2],points[-1])
        # if(sum_degree>=2*pi-0.0001 and sum_degree<=2*pi+0.0001):
        if(sum_degree==2*pi):
            return True
        else:
            return False

    def get_degree(self,x0,y0,x1,y1,x2,y2):
        d=abs(atan2(y1-y0,x1-x0)-atan2(y2-y0,x2-x0))
        if d>pi:
            return 2*pi-d
        else:
            return d


    def ErrorMessage(self):       
        # self.EM=QMessageBox()
        # self.EM.setText('invalid parameters')
        # self.EM.exec_()
        ok_flag=False

    def drawRect(self,qp,centerX,centerY,width,height):
        '''drawing rectangle'''

        #set color                  
        qp.setBrush(QtGui.QColor('red'))

        # draw
        qp.drawRect(centerX-width/2,centerY-height/2,width,height)

    def drawCircle(self,qp,centerX,centerY,radius):
        #set color                  
        qp.setBrush(QtGui.QColor('green'))
            
        # draw
        qp.drawEllipse(centerX-radius,centerY-radius,radius*2,radius*2)

        
    def drawEllipse(self,qp,centerX,centerY,radiusX,radiusY,angle):
        '''drawing ellipse'''

        #set color                  
        qp.setBrush(QtGui.QColor('yellow'))

        # draw
        
        qp.translate(centerX,centerY)
        qp.rotate(angle)
        qp.drawEllipse(-radiusX,-radiusY,radiusX*2,radiusY*2)
        qp.rotate(-angle)
        qp.translate(-centerX,-centerY)

       

    def drawTriangle(self, event, qp, args):
        '''drawing rectangle'''

        # # change border color
        # if args['color']:
        #     qp.setPen(QtGui.QColor(args['color']))
        # else:
        #     qp.setPen(QtCore.Qt.NoPen)
            
        # change fill color
        if args['fill']:
            qp.setBrush(QtGui.QColor(args['fill']))
        else:
            qp.setBrush(QtCore.Qt.NoBrush)

        # create polygon
        
        x1 = args['x']
        y1 = args['y']+args['height']
        x2 = args['x']+args['width']
        y2 = y1
        x3 = x1+(args['width']/2.0)
        y3 = args['y']

        points = QtGui.QPolygon([
            QtCore.QPoint(x1, y1),
            QtCore.QPoint(x2, y2),
            QtCore.QPoint(x3, y3),
            QtCore.QPoint(x1, y1)
        ])        

        # draw
        qp.drawPolygon(points)
        
    def drawPolygon(self, qp, *points):
        '''drawing polygon'''

        #set color                  
        qp.setBrush(QtGui.QColor('blue'))

        temp_list=[]
        # # create polygon
        num=points.__len__()/2
        for i in range(0,num):
            temp_list.append(QPoint(points[2*i],points[2*i+1]))        

        # draw
        qp.drawConvexPolygon(QPolygon(temp_list))
        
   
            

# --- main ---

class InputParametersDialog(QtGui.QDialog):
    
    def __init__(self,shapetype):
        super(InputParametersDialog, self).__init__()
        self.type=shapetype
        self.flag=False
        self.setWindowTitle("Input Parameters")
        if self.type=='Circle':
            self.centerX=200
            self.centerY=200
            self.radius=20
            
            centerLabel=QtGui.QLabel('Center Point Index')
            self.centerXEdit=QtGui.QLineEdit()
            self.centerYEdit=QtGui.QLineEdit()
            radiusLabel=QtGui.QLabel('Radius')
            self.radiusEdit=QtGui.QLineEdit()
            self.okButton=QPushButton("&OK")
            self.okButton.clicked.connect(self.OkButtonClicked)

            self.grid=QtGui.QGridLayout()
            self.grid.addWidget(centerLabel,0,0)
            self.grid.addWidget(self.centerXEdit,0,1)
            self.grid.addWidget(self.centerYEdit,0,2)
            self.grid.addWidget(radiusLabel,1,0)
            self.grid.addWidget(self.radiusEdit,1,1)
            self.grid.addWidget(self.okButton,2,1)


        elif self.type=='Rectangle':
            self.centerX=100
            self.centerY=100
            self.width=100
            self.height=100

            centerLabel=QtGui.QLabel('Center Point Index')
            self.centerXEdit=QtGui.QLineEdit()
            self.centerYEdit=QtGui.QLineEdit()
            widthLabel=QtGui.QLabel('Width')
            heightLabel=QLabel('Height')
            self.widthEdit=QtGui.QLineEdit()
            self.heightEdit=QtGui.QLineEdit()
            self.okButton=QPushButton("&OK")
            self.okButton.clicked.connect(self.OkButtonClicked)

            self.grid=QtGui.QGridLayout()
            self.grid.addWidget(centerLabel,0,0)
            self.grid.addWidget(self.centerXEdit,0,1)
            self.grid.addWidget(self.centerYEdit,0,2)
            self.grid.addWidget(widthLabel,1,0)
            self.grid.addWidget(self.widthEdit,1,1)
            self.grid.addWidget(heightLabel,2,0)
            self.grid.addWidget(self.heightEdit,2,1)
            self.grid.addWidget(self.okButton,3,1)
        
        elif self.type=='Ellipse':
            self.centerX=100
            self.centerY=100
            self.radiusX=100
            self.radiusY=100
            self.angle=0

            centerLabel=QtGui.QLabel('Center Point Index')
            self.centerXEdit=QtGui.QLineEdit()
            self.centerYEdit=QtGui.QLineEdit()
            widthLabel=QtGui.QLabel('RadiusX')
            heightLabel=QLabel('RadiusY')
            self.widthEdit=QtGui.QLineEdit()
            self.heightEdit=QtGui.QLineEdit()
            angleLabel=QLabel('Rotate angle')
            self.angleEdit=QLineEdit()
            self.okButton=QPushButton("&OK")
            self.okButton.clicked.connect(self.OkButtonClicked)

            self.grid=QtGui.QGridLayout()
            self.grid.addWidget(centerLabel,0,0)
            self.grid.addWidget(self.centerXEdit,0,1)
            self.grid.addWidget(self.centerYEdit,0,2)
            self.grid.addWidget(widthLabel,1,0)
            self.grid.addWidget(self.widthEdit,1,1)
            self.grid.addWidget(heightLabel,2,0)
            self.grid.addWidget(self.heightEdit,2,1)
            self.grid.addWidget(angleLabel,3,0)
            self.grid.addWidget(self.angleEdit,3,1)
            self.grid.addWidget(self.okButton,4,1)

        elif self.type=='Polygon':
            self.points=[]
            PointLabel=QLabel('Input Coordinates of Points in order')
            self.PointEdit=QLineEdit()
            self.okButton=QPushButton("&OK")
            self.okButton.clicked.connect(self.OkButtonClicked)

            self.grid=QtGui.QGridLayout()
            self.grid.addWidget(PointLabel,0,0)
            self.grid.addWidget(self.PointEdit,1,0)
            self.grid.addWidget(self.okButton,2,0)

    
        self.setLayout(self.grid)
        self.show()

    def OkButtonClicked(self):
        if self.type=='Circle':
            self.centerX=int(self.centerXEdit.text())
            self.centerY=int(self.centerYEdit.text())
            self.radius=int(self.radiusEdit.text())
            print self.centerX,self.centerY,self.radius
            MyCanvas().CircleGenerator(self.centerX,self.centerY,self.radius)
            self.close()

        elif self.type=='Rectangle':
            self.centerX=int(self.centerXEdit.text())
            self.centerY=int(self.centerYEdit.text())
            self.width=int(self.widthEdit.text())
            self.height=int(self.heightEdit.text())
            print self.centerX,self.centerY,self.width,self.height
            MyCanvas().RectangleGenerator(self.centerX,self.centerY,self.width,self.height)
            self.close()

        elif self.type=='Ellipse':
            self.centerX=int(self.centerXEdit.text())
            self.centerY=int(self.centerYEdit.text())
            self.radiusX=int(self.widthEdit.text())
            self.radiusY=int(self.heightEdit.text())
            self.angle=int(self.angleEdit.text())
            print self.centerX,self.centerY,self.radiusX,self.radiusY,self.angle
            MyCanvas().EllipseGenerator(self.centerX,self.centerY,self.radiusX,self.radiusY,self.angle)
            self.close()

        elif self.type=='Polygon':
            # print self.PointEdit.text()
            str=re.findall(r"\d+\.?\d*",self.PointEdit.text())
            # print self.str
            for i in range(0,str.__len__()):
                self.points.append(int(str[i]))
            print self.points
            MyCanvas().PolygonGenerator(*self.points)
            self.close()

        self.flag=True






class App(QtGui.QWidget):

    def __init__(self):
        super(App, self).__init__()

        self.initUI()
    def restart(self):     

        for item in ShapeBase:
            if item[0]=='Ellipse':
                while(True):               
                    a=random.randint(0,Width)
                    b=random.randint(0,Height)
                    c=random.randint(0,360)     
                    if self.canvas.EllipseGenerator(a,b,item[1],item[2],c):
                        break
            elif item[0]=='Circle':
                while(True):
                    a=random.randint(0,Width)
                    b=random.randint(0,Height)     
                    if self.canvas.CircleGenerator(a,b,item[1]):
                        break
            elif item[0]=='Rectangle':
                while(True):
                    a=random.randint(0,Width)
                    b=random.randint(0,Height)
                    c=random.randint(0,360)
                    co=cos(c/180.0*pi)
                    si=sin(c/180.0*pi)
                    w=float(item[1])
                    h=float(item[2])
                    points=[w/2,h/2,-w/2,h/2,-w/2,-h/2,w/2,-h/2]
                    new_points=[]
                    for i in range(0,points.__len__()/2):
                        new_points.append(int(points[2*i]*co+points[2*i+1]*si+a))
                        new_points.append(int(points[2*i]*(-si)+points[2*i+1]*co+b))
                    if self.canvas.PolygonGenerator(*new_points):
                        break
            elif item[0]=='Polygon' or 'Triangle':
                while(True):
                    a=random.randint(0,Width)
                    b=random.randint(0,Height)
                    c=random.randint(0,360)
                    co=cos(c/180.0*pi)
                    si=sin(c/180.0*pi)
                    points=[]
                    for i in range(1,item.__len__()):
                        points.append(item[i])                    
                    new_points=[]
                    for i in range(0,points.__len__()/2):
                        new_points.append(int(points[2*i]*co+points[2*i+1]*si+a))
                        new_points.append(int(points[2*i]*(-si)+points[2*i+1]*co+b))
                    if self.canvas.PolygonGenerator(*new_points):
                        break
        

    def CircleChose(self):

        self.Dialog=InputParametersDialog('Circle')
        # if self.Dialog.flag==True:
        #     self.canvas.CircleGenerator(self.Dialog.centerX,self.Dialog.centerY,self.Dialog.radius)
        

    def EllipseChose(self):
        self.Dialog=InputParametersDialog('Ellipse')
        # if self.Dialog.flag==True:        
        #     self.canvas.EllipseGenerator(200,200,150,50,60)


    def RectangleChose(self):

        self.Dialog=InputParametersDialog('Rectangle')
        # if self.Dialog.flag==True:
        #     self.canvas.RectangleGenerator(200,200,40,40)


    def TriangleChose(self):
        pass

    def PolygonChose(self):
        self.Dialog=InputParametersDialog('Polygon')
        # if self.Dialog.flag==True:
        #     self.canvas.PolygonGenerator(30,30,100,0,200,50,50,200,0,100)

    def RandomShapeChose(self):
        pass
    


    def initUI(self):      

        self.vbox = QtGui.QVBoxLayout(self)
        self.setLayout(self.vbox)

        #--- canvas - created to get tool list ---
        
        self.canvas = MyCanvas() 

        
        self.restart()
                
            


        # self.ShapeChoice=[
        #     ('Circle',self.CircleChose),
        #     ('Ellipse',self.EllipseChose),
        #     ('Rectangle',self.RectangleChose),
        #     # ('Triangle',self.TriangleChose),
        #     ('Polygon',self.PolygonChose),
        #     # ('RandomShape',self.RandomShapeChose)
        # ]

        

        # #--- tool buttons ---        
        # self.hboxTools = QtGui.QHBoxLayout()

        # for name,func in self.ShapeChoice:
        #     btn = QtGui.QPushButton(name)
        #     btn.setCheckable(True)
        #     btn.setAutoExclusive(True) 
        #     btn.clicked.connect(func)
        #     self.hboxTools.addWidget(btn)

        #     if name == 'RandomShape':
        #         btn.setChecked(True)
        

        # self.btnToolsGroup = QtGui.QGroupBox("Shape")
        # self.btnToolsGroup.setLayout(self.hboxTools)
        # self.vbox.addWidget(self.btnToolsGroup)
    

        self.btn=QPushButton("restart")
        self.btn.setCheckable(True)
        self.btn.setAutoExclusive(True)
        self.btn.clicked.connect(self.restart)

         #--- canvas - add to window ---
        self.vbox.addWidget(self.canvas)
        self.vbox.addWidget(self.btn)
       
        
        #self.setGeometry(300, 300, 600, 170)
        self.setWindowTitle('MyCanvas')
        self.show()

        

        
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
