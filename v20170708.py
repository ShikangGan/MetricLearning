#!/usr/bin/env python3

# http://zetcode.com/gui/pyqt4/drawing/
# https://pl.python.org/forum/index.php?topic=6010.msg25683#msg25683

# maybe better to use QGraphicsView, QGraphicsScene, QGraphicsItem

import sys
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
class MyCanvas(QtGui.QWidget):
    
    shapes=[]
    
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
        for shape in self.shapes:
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
            self.shapes.append(('circle',centerX,centerY,radius))
            self.update()
            # self.DrawPicture()
            
        else:
            self.ErrorMessage()

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
                # if ((i*co+j*si-centerX)**2.0/(radiusX**2.0)+(-i*si+j*co-centerY)**2.0/(radiusY**2.0)) <= 1:
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
          
            self.shapes.append(('ellipse',centerX,centerY,radiusX,radiusY,angle))
            self.update()
        else:
            self.ErrorMessage()

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
            
            self.shapes.append(('rectangle',centerX,centerY,width,height))
            self.update()
        else:
            self.ErrorMessage()


    def PolygonGenerator(self,*points):
        flag=True
        exit_flag=False
        x1=min(points[0::2])
        x2=max(points[0::2])
        y1=min(points[1::2])
        y2=max(points[1::2])
        num=points.__len__()
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
            self.shapes.append(('polygon',points))
            self.update()
        else:
            self.ErrorMessage()


    def ifInPolygon(self,x,y,*points):
        sum_degree=0
        num=points.__len__()/2
        for i in range(0,num-1):
            sum_degree+=self.get_degree(x,y,points[2*i],points[2*i+1],points[2*i+2],points[2*i+3])
        sum_degree+=self.get_degree(x,y,points[0],points[1],points[-2],points[-1])
        if(sum_degree>=2*pi-0.01 and sum_degree<=2*pi+0.01):
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
        print 'invalid parameters'

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
        qp.drawEllipse(centerX,centerY,radius,radius)

        
    def drawEllipse(self,qp,centerX,centerY,radiusX,radiusY,angle):
        '''drawing ellipse'''

        #set color                  
        qp.setBrush(QtGui.QColor('yellow'))

        # draw
        
        qp.translate(centerX,centerY)
        qp.rotate(angle)
        qp.drawEllipse(-radiusX/2,-radiusY/2,radiusX,radiusY)
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

class App(QtGui.QWidget):

    def __init__(self):
        super(App, self).__init__()

        self.initUI()

    def CircleChose(self):
        Dial=QtGui.QDialog(self)
        Dial.setWindowTitle('Circle Parameters')

        centerLabel=QtGui.QLabel('Center Point Index')
        centerXEdit=QtGui.QLineEdit()
        centerYEdit=QtGui.QLineEdit()
        radiusLabel=QtGui.QLabel('Radius')
        radiusEdit=QtGui.QLineEdit()
        # buttonBox =QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok|QtGui.QDialogButtonBox.Cancel)
        okButton=QPushButton("&OK")
        # cancelButton=QPushButton("&Cancel")

        grid=QtGui.QGridLayout()
        grid.addWidget(centerLabel,0,0)
        grid.addWidget(centerXEdit,0,1)
        grid.addWidget(centerYEdit,0,2)
        grid.addWidget(radiusLabel,1,0)
        grid.addWidget(radiusEdit,1,1)
        grid.addWidget(okButton,2,1)
        # grid.addWidget(cancelButton,2,2)

        Dial.setLayout(grid)
        

        # print centerYEdit.text()
        self.Dialog = Dial
        self.centerXEdit = centerXEdit
        
        okButton.clicked.connect(self.get_value)
        # cancelButton.clicked.connect(Dial.close)
        if Dial.exec_():
            centerX=unicode(centerXEdit.text())
            centerY=unicode(centerYEdit.text())
            radius=unicode(radiusEdit.text())
            print centerX,centerY,radius

            
        # self.Dial.setGeometry(100,200,300,400)
        Dial.show()
        self.canvas.CircleGenerator(40,50,20)

    def get_value(self):
        print self.centerXEdit.text()

    def EllipseChose(self):
        self.canvas.EllipseGenerator(200,200,150,50,60)
    def RectangleChose(self):
        self.canvas.RectangleGenerator(200,200,40,40)
    def TriangleChose(self):
        pass
    def PolygonChose(self):
        # self.canvas.PolygonGenerator(0,0,100,0,25,25,0,100)
        self.canvas.PolygonGenerator(30,30,100,0,200,50,50,200,0,100)
    def RandomShapeChose(self):
        pass
    


    def initUI(self):      

        self.vbox = QtGui.QVBoxLayout(self)
        self.setLayout(self.vbox)

        #--- canvas - created to get tool list ---
        
        self.canvas = MyCanvas()

        self.ShapeChoice=[
            ('Circle',self.CircleChose),
            ('Ellipse',self.EllipseChose),
            ('Rectangle',self.RectangleChose),
            # ('Triangle',self.TriangleChose),
            ('Polygon',self.PolygonChose),
            # ('RandomShape',self.RandomShapeChose)
        ]

        

        #--- tool buttons ---        
        self.hboxTools = QtGui.QHBoxLayout()

        for name,func in self.ShapeChoice:
            btn = QtGui.QPushButton(name)
            btn.setCheckable(True)
            btn.setAutoExclusive(True) 
            btn.clicked.connect(func)
            self.hboxTools.addWidget(btn)

            if name == 'RandomShape':
                btn.setChecked(True)
        

        self.btnToolsGroup = QtGui.QGroupBox("Shape")
        self.btnToolsGroup.setLayout(self.hboxTools)
        self.vbox.addWidget(self.btnToolsGroup)
    

         #--- canvas - add to window ---
        self.vbox.addWidget(self.canvas)
       
        
        #self.setGeometry(300, 300, 600, 170)
        self.setWindowTitle('MyCanvas')
        self.show()

        

        
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())