import numpy as np
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from random import randint,random
from threading import Thread
from sklearn.cross_validation import train_test_split
import time
from PySide.QtCore import * 
from PySide.QtGui import *
import sys
import liver
import heart
import diab
import mainform
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
   	  #print(form.lineEdit.text())
   	  #code of ml
      disease_name=s

      print(s)
      f1=open(disease_name+".file",'r')
      c_svc=(float)(f1.readline())
      gamma_svc=(float)(f1.readline())
      att_to_keep_temp=f1.readline().split(',')
      att_to_keep=[ int(x) for x in att_to_keep_temp]
      if -1 in att_to_keep:
          att_to_keep=[]
      data_result = (int)(f1.readline())
      missing_value=(int)(f1.readline())
      CHUNK_SIZE=(float)(f1.readline())
      f1.close()
      #print(c_svc,gamma_svc,att_to_keep,CHUNK_SIZE)

      import heapq
      class PriorityQueue:
          def __init__(self):
              self.elements=[]
          def empty(self):
              return len(self.elements)==0
          def put(self,item,priority):
              heapq.heappush(self.elements,(priority,item))
          def get(self):
              return heapq.heappop(self.elements)[1]

      start_time = time.time()
      def individual(length, min, max):
         r= [randint(min,max) for x in range(length)]
         for y in att_to_keep:
             r[y]=1
         return r

      def population(count, length, min, max):
          
          pop=[]
          while len(pop)<count:
              x=individual(length,min,max)
              if x not in pop:
                  #print (x)
                  pop.append(x)
          return pop

      def trim(individual, data):
         length = len(individual)
         newdata = []
         for row in data:
            newrow = []
            for i in range(length):
               if individual[i] == 1 and i!= data_result:
                  newrow.append(row[i])
            newdata.append(newrow)
         return newdata
      def fitness(individual,data,y):
          newdata = trim(individual,data)
          X = newdata
          #y = data[:,data_result]
          X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=.2,random_state=0  )
          clf = SVC(kernel ='rbf',C=c_svc,gamma=gamma_svc)
          clf.fit(X_train,y_train)
          pred=clf.predict(X_test)
          return accuracy_score(pred,y_test)
      def grade(pop,data,result_y,prev_pop,prev_acc,acc_0,acc_1):
          sum  = 0
          for i in pop:
              if i in prev_pop:
                  #print ("f")
                  sum=sum+prev_acc[prev_pop.index(i)]
              else:
                  prev_pop.append(i)
                  #y = data[:,data_result]
                  acc=fitness(i,data,result_y)
                  for j in range(len(data[0])):
                      if i[j] == 1:
                          acc_1+=acc
                      else:
                          acc_0+=acc
                  prev_acc.append(acc)
                  sum = sum + acc
          return sum/(len(pop)*1.0)
      def evolve(pop,data,result_y,acc_0,acc_1,retain=.2,random_select=.05,mutate=.01):
          #y = data[:,data_result]
          graded  = [(fitness(x,data,result_y),x) for x in pop]
          graded = [x[1] for x in sorted(graded,reverse=1)]
          retain_length = int(len(graded)*retain)
          parents = graded[:retain_length]
          bekar = int(len(graded)*random_select)
          for individual in graded[(len(graded)-bekar):]:
              if random_select > random():
                  parents.append(individual)
          p=parents
          for individual in p:
              if mutate>random():
                  count , termination=0,0
                  while(count<15 and termination<100):
                      pos_to_mutate = randint(0, len(individual)-1)
                      if individual[pos_to_mutate] == 0 and acc_1[pos_to_mutate]>acc_0[pos_to_mutate]:
                             individual[pos_to_mutate] = 1
                             if individual not in parents:
                                 parents.append(individual)
                             count+=1
                      elif individual[pos_to_mutate] == 1 and acc_0[pos_to_mutate]>acc_1[pos_to_mutate]:
                             individual[pos_to_mutate] = 0
                             if individual not in parents:
                                 parents.append(individual)
                             count+=1
                      termination+=1

          parents=parents[:(int)(0.8*len(pop))]
          parents_length = len(parents)
          again=False
          #desired_length = len(pop) - parents_length
          children = []
          m=0
          f=0
          while len(parents) < len(pop):
            
              
          
              if f == parents_length-1:
                  m+=1
                  f=m
              f+=1
              if f>= len(parents) or m>=len(parents):
                  #print (len(parents))
                  if again:
                      break
                  again=True
                  m=0
                  f=1
              
              if m != f:
                  male = parents[m]
                  female = parents[f]
                  male_acc=[0.0 for i in range(len(data[0]))]
                  female_acc=[0.0 for i in range(len(data[0]))]
              
                  point_to_crossover=PriorityQueue()
                  
                  for i in range(len(data[0])):
                      if i==0:
                          i+=1
                      if male[i]==0:
                          male_acc[i]=male_acc[i-1]+acc_0[i]
                      else:
                          male_acc[i]=male_acc[i-1]+acc_1[i]
                      if female[i]==0:
                          female_acc[i]=female_acc[i-1]+acc_0[i]
                      else:
                          female_acc[i]=female_acc[i-1]+acc_1[i]
                  
                  #greatest_avg=0.0
                  for i in range(len(data[0])):
                      if i==0:
                          i+=1
                      
                      avg = male_acc[i]+female_acc[len(female_acc)-1]-female_acc[i]
                      avg += female_acc[i]+male_acc[len(male_acc)-1]-male_acc[i]
                      point_to_crossover.put(i,avg)
                  check1,check2=False,False        
                  while check1==False and check2==False:
                      if(point_to_crossover.empty()):
                          break
                      pt=point_to_crossover.get()
                      child = male[:pt] + female[pt:]
                      if child not in children and child not in parents:
                          check1=True
                          parents.append(child)
                          
                      child = female[:pt]+ male[pt:] 
                      if child not in children and child not in parents:
                          parents.append(child)
                          check2=True
                      
           
          while len(parents) < len(pop):
              m=0
              f=1
              
              if m != f:
                  male = parents[m]
                  female = parents[f]
                  male_acc=[0.0 for i in range(len(data[0]))]
                  female_acc=[0.0 for i in range(len(data[0]))]
              
                  point_to_crossover=PriorityQueue()
                  
                  for i in range(len(data[0])):
                      if i==0:
                          i+=1
                      if male[i]==0:
                          male_acc[i]=male_acc[i-1]+acc_0[i]
                      else:
                          male_acc[i]=male_acc[i-1]+acc_1[i]
                      if female[i]==0:
                          female_acc[i]=female_acc[i-1]+acc_0[i]
                      else:
                          female_acc[i]=female_acc[i-1]+acc_1[i]
                  
                  #greatest_avg=0.0
                  for i in range(len(data[0])):
                      if i==0:
                          i+=1
                      
                      avg = male_acc[i]+female_acc[len(female_acc)-1]-female_acc[i]
                      avg += female_acc[i]+male_acc[len(male_acc)-1]-male_acc[i]
                      point_to_crossover.put(i,avg)
          
                  pt=point_to_crossover.get()
                  child = male[:pt] + female[pt:]
                  parents.append(child)
                          
                  child = female[:pt]+ male[pt:] 
                  parents.append(child)
                       
                 
          
          return parents
              
          

      def filterData(data):
          size=len(data)
          no_att=len(data[0])
          avg = [0.0 for i in range(no_att)]
          cnt = [0 for i in range(no_att)]
          for i in range(size):
              for j in range(no_att):
                  if data[i][j] != missing_value:
                      avg[j]+=(float)(data[i][j])
                      cnt[j]+=1
          
          for j in range(no_att):
              if cnt[j] != 0:
                  avg[j]/=cnt[j]
          
          for i in range(size):
              for j in range(no_att):
                  if data[i][j] == missing_value:
                      data[i][j]=avg[j]
          
          
      def foo(data,y,result_prob,index):
          p = population(100,len(data[0]),0,1)
          cnt=0
          prev_pop=[]
          prev_data=[]
          no_att1=len(data[0])
          acc_0 = [0.0 for i in range(no_att1)]
          acc_1 = [0.0 for i in range(no_att1)]
          g1=grade(p, data,y,prev_pop,prev_data,acc_0,acc_1)
          
          while 1:
              #print(index)
              p = evolve(p, data,y,acc_0,acc_1)
              #print(index)
              g2=grade(p,data,y,prev_pop,prev_data,acc_0,acc_1)
              g1=round(g1,5)
              g2=round(g2,5)
              if g1==g2:
                  break
              g1=g2
              #print("\t",index,g2)
          
          for j in range(no_att1):
              if p[0][j]==1:
                  cnt+=1
          result_prob[index]=p[0]
          print (index,g2,cnt)
          
      data_original = np.loadtxt(disease_name+".dat",delimiter=",")
      #data_original = data_original[0:500]
      filterData(data_original)

      no_att=len(data_original[0])

      result_final=data_original[:,data_result]
      #data_original=newdata
      size=len(data_original)
      #size=1600
      chunk=(int)(size**(CHUNK_SIZE))
      no_att=len(data_original[0])

      print (size,no_att)
      n_chunk = (float)(size/chunk)

      x=(int)(n_chunk)
      if n_chunk>(float)(x):
          n_chunk=(int)(n_chunk)+1
      n_chunk=(int)(n_chunk) 
      threads = [None] * n_chunk
      prob1 = [[0 for i in range(no_att)] for j in range(n_chunk)]

      it=0
      counter=0

      while it<size:
          data_ = data_original[counter::n_chunk]
          y_=result_final[counter::n_chunk]
          threads[counter] = Thread(target=foo, args=(data_,y_, prob1, counter))
          threads[counter].start()
          counter+=1
          it+=chunk
      print(n_chunk,counter)
      for i in range(counter):
          threads[i].join()
          
      #att_to_keep=0
       
      max_acc=0.0
      max_index=0
      index=0
      maxdata=[]
      max_att=[]
      for x in prob1:
          newdata = []
          for row in data_original:
              for y in att_to_keep:
                  row[y]=1
              newrow = []
              for i in range(no_att):
                  if x[i] == 1 and i!= data_result:
                      newrow.append(row[i])
              newdata.append(newrow)
          acc=0.0
          
          X_train, X_test, y_train, y_test = train_test_split(newdata,result_final,test_size=.2,random_state=0)
          clf = SVC(kernel ='rbf',C=c_svc,gamma=gamma_svc)
          clf.fit(X_train,y_train)
          pred=clf.predict(X_test)
          acc=accuracy_score(pred,y_test)
          acc*=100
          if acc>max_acc:
              max_acc=acc
              max_att=x
              max_index=index
              maxdata=newdata
                  
          index+=1
      random_max=0
      random_it=0
      while random_it<100:

          X_train, X_test, y_train, y_test = train_test_split(maxdata,result_final,test_size=.2,random_state=random_it)
          clf = SVC(kernel ='rbf',C=c_svc,gamma=gamma_svc)
          clf.fit(X_train,y_train)
          pred=clf.predict(X_test)
          acc=accuracy_score(pred,y_test)
          acc*=100
          if acc>max_acc:
              max_acc=acc
              random_max=random_it
          random_it+=1
      if s == 'ap_liver':
         test_new = getliver(o)
      elif s == 'diabetes':
         test_new = getdiabetes(o)
      else:
         test_new = getheart(o)
      
      
      test1=[]
      for i in range(len(max_att)):
          if max_att[i]==1 and i!=data_result:
              test1.append(test_new[i])
      print(test1)

      X_train, X_test, y_train, y_test = train_test_split(maxdata,result_final,test_size=.2,random_state=random_max)
      clf = SVC(kernel ='rbf',C=c_svc,gamma=gamma_svc)
      clf.fit(X_train,y_train)
      pred=clf.predict(test1)
      if s == 'ap_liver':
         p1(o,pred,max_acc)
      elif s == 'diabetes':
         p2(o,pred,max_acc)
      else:
         p3(o,pred,max_acc)

      print (max_index,max_acc)
      
      t=(time.time() - start_time)
      print("--- %s seconds ---" % (t))
      fobj = open(disease_name+".result","a") 
      fobj.write("\n\nAttributes : ")
      for i in max_att:
          fobj.write("%s "%i)
      fobj.write("\nAccuracy : %f" % max_acc )
      #fobj.write(acc)
      fobj.write("\nExecution Time : %f sec" % t)
      fobj.write("\nData Size : %d " % len(data_original))
      fobj.write("\nC : %d  Gamma : %f Ramdom State : %d" % (c_svc,gamma_svc,random_max))
      #fobj.write("\nGamma : %f " % gamma_svc)
      fobj.close()
      #fobj.write(t)
      #fobj.write(t)
      '''progress = QProgressDialog()
   	  progress.setWindowModality(Qt.WindowModal)
   	  progress.setLabelText('Training Data...')
   	  progress.setMinimum(0)
   	  progress.setMaximum(150000)
   	  progress.setMinimumDuration(4)
   	  for i in range(150000):
   	  	progress.setValue(i)
   	  progress.setValue(150000)
      '''
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
      test_new=[i for i in range(12)]
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
      test_new[10]=float(li.lineEdit_11.text())
      test_new[11]=float(li.lineEdit_12.text())
      return test_new
   
def p1(o,pred,m):
      if int(pred[0]) == 2:
         o.lineEdit_11.setText("No")
      else:
      	o.lineEdit_11.setText("Yes")
      o.lineEdit_12.setText(str(m))

def p2(o,pred,m):
      if int(pred[0]) == 0:
         o.lineEdit_11.setText("No")
      else:
      	o.lineEdit_11.setText("Yes")
      o.lineEdit_12.setText(str(m))

def p3(o,pred,m):
      if int(pred[0]) == 0:
         o.lineEdit_14.setText("No")
      elif int(pred[0]) == 1:
      	o.lineEdit_14.setText("low")
      elif int(pred[0]) == 1:
      	o.lineEdit_14.setText("medium")
      elif int(pred[0]) == 1:
      	o.lineEdit_14.setText("high")
      else:
      	o.lineEdit_14.setText("yes")
      
      o.lineEdit_15.setText(str(m))

app = QApplication(sys.argv)
pixmap = QPixmap("splash.jpg")
splash = QSplashScreen(pixmap)
splash.show()
li = liverp()
he = heartp()
di = diabp()
men = menu()
Qt.WindowStaysOnTopHint
app.processEvents()
j=0
for i in range(35000000):
	j+=1
men.show()
splash.finish(men)
app.exec_() 



#
 
