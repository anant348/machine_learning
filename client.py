import sys
from PySide.QtCore import * 
from PySide.QtGui import *
import liver
import heart
import diab
import mainform
import urllib.request
import t
def fun():
      li.click.emit('ap_liver',li)
def fun1():
   he.click.emit('heart_clev',he)
def fun2():
   di.click.emit('diabetes',di)

class liverp(QDialog,liver.Ui_Form):
   click = Signal(str,object)
   def __init__(self,parent=None):
      super(liverp,self).__init__(parent)
      self.setupUi(self)
      #self.connect(self.pushButton,SIGNAL(""),self.eval())
      self.pushButton.clicked.connect(fun)
      self.click.connect(eval)
      self.backButton.clicked.connect(backl)
   
class progr(QWidget,t.Ui_Form):
    click = Signal(str,object)
    def __init__(self,parent=None):
      super(progr,self).__init__(parent)
      
      self.setupUi(self)
      self.click.connect(eval)
      #self.connect(self.pushButton,SIGNAL(""),self.eval())
      
class heartp(QDialog,heart.Ui_Form):
   click = Signal(str,object)
   def __init__(self,parent=None):
      super(heartp,self).__init__(parent)
      self.setupUi(self)
      #self.connect(self.pushButton,SIGNAL(""),self.eval())
      self.pushButton.clicked.connect(fun1)
      self.click.connect(eval)
      self.backButton.clicked.connect(backh)   

class diabp(QDialog,diab.Ui_Form):
   click = Signal(str,object)
   def __init__(self,parent=None):
      super(diabp,self).__init__(parent)
      self.setupUi(self)
      #self.connect(self.pushButton,SIGNAL(""),self.eval())
      self.pushButton.clicked.connect(fun2)
      self.click.connect(eval)
      self.backButton.clicked.connect(backd)

class menu(QDialog,mainform.Ui_Form):
  def __init__(self,parent=None):
    super(menu,self).__init__(parent)
    self.setupUi(self)
    self.pushButton.clicked.connect(next)

def next():
  men.hide()
  if men.radioButton.isChecked():
    di.show()
  elif men.radioButton_2.isChecked():
    he.show()
  else:
    li.show()  
       

def backl():
   li.hide()
   men.show()
def backh():
   he.hide()
   men.show()
def backd():
   di.hide()
   men.show()
   
def eval(s,o):
      if s == 'ap_liver':
         test_new = getliver(o)
      elif s == 'diabetes':
         test_new = getdiabetes(o)
      else:
         test_new = getheart(o)
      test_new=str(test_new)
      test_new=test_new.replace(" ","")
      result = urllib.request.urlopen("http://192.168.137.144:8000/?q="+s+"&data="+test_new).read()
      result=str(result)
      result=result[2:-1]
      if s == 'ap_liver':
         p1(o,result)
      elif s == 'diabetes':
         p2(o,result)
      else:
         p3(o,result)

def getliver(li):
      test_new=[i for i in range(10)]
      test_new[0]=float(li.lineEdit.text())
      test_new[1]=float(li.lineEdit_2.text())
      test_new[2]=float(li.lineEdit_3.text())
      test_new[3]=float(li.lineEdit_4.text())
      test_new[4]=float(li.lineEdit_5.text())
      test_new[5]=float(li.lineEdit_6.text())
      test_new[6]=float(li.lineEdit_7.text())
      test_new[7]=float(li.lineEdit_8.text())
      test_new[8]=float(li.lineEdit_9.text())
      test_new[9]=float(li.lineEdit_10.text())
      return test_new
def getdiabetes(li):
      test_new=[i for i in range(8)]
      test_new[0]=float(li.lineEdit.text())
      test_new[1]=float(li.lineEdit_2.text())
      test_new[2]=float(li.lineEdit_3.text())
      test_new[3]=float(li.lineEdit_4.text())
      test_new[4]=float(li.lineEdit_5.text())
      test_new[5]=float(li.lineEdit_6.text())
      test_new[6]=float(li.lineEdit_7.text())
      test_new[7]=float(li.lineEdit_8.text())
      return test_new
def getheart(li):
      test_new=[i for i in range(13)]
      test_new[0]=float(li.lineEdit.text())
      test_new[1]=float(li.lineEdit_2.text())
      test_new[2]=float(li.lineEdit_3.text())
      test_new[3]=float(li.lineEdit_4.text())
      test_new[4]=float(li.lineEdit_5.text())
      test_new[5]=float(li.lineEdit_6.text())
      test_new[6]=float(li.lineEdit_13.text())
      test_new[7]=float(li.lineEdit_7.text())
      test_new[8]=float(li.lineEdit_8.text())
      test_new[9]=float(li.lineEdit_9.text())
      test_new[10]=float(li.lineEdit_10.text())
      test_new[11]=float(li.lineEdit_11.text())
      test_new[12]=float(li.lineEdit_12.text())
      return test_new
   
def p1(o,m):
      pred = m.split(",")
      if int(pred[0]) == 2:
         o.lineEdit_11.setText("No")
      else:
         o.lineEdit_11.setText("Yes")
      o.lineEdit_12.setText(str(pred[1]))

def p2(o,m):
      pred = m.split(",")
      if int(pred[0]) == 0:
         o.lineEdit_11.setText("No")
      else:
         o.lineEdit_11.setText("Yes")
      o.lineEdit_12.setText(str(pred[1]))

def p3(o,m):
      pred = m.split(",")
      if int(pred[0]) == 1:
         o.lineEdit_14.setText("No")
      else:
         o.lineEdit_14.setText("yes")
      
      o.lineEdit_15.setText(str(pred[1]))

app = QApplication(sys.argv)
pixmap = QPixmap("splash.jpg")
splash = QSplashScreen(pixmap)
splash.show()
li = liverp()
he = heartp()
di = diabp()
men = menu()
pro=progr()
Qt.WindowStaysOnTopHint
app.processEvents()
j=0
for i in range(35000000):
   j+=1
men.show()
splash.finish(men)

app.exec_() 



#
 
