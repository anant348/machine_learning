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
import urllib.request
def f():
 i=8
 #progress.show()

app = QApplication(sys.argv)
progress = QProgressDialog()
#progress.setWindowModality(Qt.WindowModal)
progress.setLabelText('Training Data...')
progress.setMinimum(0)
progress.setMaximum(0)
progress.setMinimumDuration(1)
f()



app.exec_() 
