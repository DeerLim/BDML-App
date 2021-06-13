# -*- coding: utf-8 -*-
"""HDSSL_WDBC.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Pya1NkhxWlphXzpzjc_JCtMthJygzdO5
"""

# !pip install docplex
# !pip install qiskit

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.sparse.csgraph import laplacian
import copy

# Reading data from 5 nodes
df1 = pd.read_excel('/content/drive/MyDrive/Colab Notebooks/MLdata/WDBCData/node1.xlsx')
df2 = pd.read_excel('/content/drive/MyDrive/Colab Notebooks/MLdata/WDBCData/node2.xlsx')
df3 = pd.read_excel('/content/drive/MyDrive/Colab Notebooks/MLdata/WDBCData/node3.xlsx')
df4 = pd.read_excel('/content/drive/MyDrive/Colab Notebooks/MLdata/WDBCData/node4.xlsx')
df5 = pd.read_excel('/content/drive/MyDrive/Colab Notebooks/MLdata/WDBCData/node5.xlsx')

# df1 = pd.read_excel('./node1.xlsx')
# df2 = pd.read_excel('./node2.xlsx')
# df3 = pd.read_excel('./node3.xlsx')
# df4 = pd.read_excel('./node4.xlsx')
# df5 = pd.read_excel('./node5.xlsx')

df1.shape, df2.shape, df3.shape, df4.shape, df5.shape

node1 = np.asmatrix(df1)
node2 = np.asmatrix(df2)
node3 = np.asmatrix(df3)
node4 = np.asmatrix(df4)
node5 = np.asmatrix(df5)

np.random.shuffle(node1)
np.random.shuffle(node2)
np.random.shuffle(node3)
np.random.shuffle(node4)
np.random.shuffle(node5)

train_node1 = node1
train_node2 = node2
train_node3 = node3
train_node4 = node4
train_node5 = node5

ry1, ry2, ry3, ry4, ry5 = copy.deepcopy(node1[:,30]), copy.deepcopy(node2[:,30]), copy.deepcopy(node3[:,30]), copy.deepcopy(node4[:,30]), copy.deepcopy(node5[:,30])

# parameters setting
y_size = 100  #numbers of y_i
lamda = 10^(-3)
eta = 10^(-4)
rho = 10^(-3)
L = 50

for i in range(y_size, len(train_node1)):
  train_node1[i,30] = 0
  train_node2[i,30] = 0
  train_node3[i,30] = 0
  train_node4[i,30] = 0

for i in range(y_size, len(train_node5)):
  train_node5[i,30] = 0

H1, H2, H3, H4, H5 = train_node1[:,0:30], train_node2[:,0:30], train_node3[:,0:30], train_node4[:,0:30], train_node5[:,0:30]
y1, y2, y3, y4, y5 = train_node1[:,30], train_node2[:,30], train_node3[:,30], train_node4[:,30], train_node5[:,30]
I = np.identity(30)
C = np.zeros((114, 114))
C5 = np.zeros((113, 113))
L1, L2, L3, L4, L5 = laplacian(H1.dot(H1.transpose()), normed=True), laplacian(H2.dot(H2.transpose()), normed=True), laplacian(H3.dot(H3.transpose()), normed=True), laplacian(H4.dot(H4.transpose()), normed=True), laplacian(H5.dot(H5.transpose()), normed=True)

for i in range(0,y_size+1):
  C[i,i]=1
  C5[i,i]=1

H1.shape, y1.shape, I.shape, C.shape, C5.shape, L1.shape, ry1.shape

temp1 = H1.transpose().dot(C).dot(H1) + eta * H1.transpose().dot(L1).dot(H1) + lamda * I
temp2 = H2.transpose().dot(C).dot(H2) + eta * H2.transpose().dot(L2).dot(H2) + lamda * I
temp3 = H3.transpose().dot(C).dot(H3) + eta * H3.transpose().dot(L3).dot(H3) + lamda * I
temp4 = H4.transpose().dot(C).dot(H4) + eta * H4.transpose().dot(L4).dot(H4) + lamda * I
temp5 = H5.transpose().dot(C5).dot(H5) + eta * H5.transpose().dot(L5).dot(H5) + lamda * I

P1_inv, P2_inv, P3_inv, P4_inv, P5_inv = np.linalg.inv(temp1), np.linalg.inv(temp2), np.linalg.inv(temp3), np.linalg.inv(temp4), np.linalg.inv(temp5)

z = np.zeros((30,1))
r1, r2, r3, r4, r5 = np.zeros((30,1)), np.zeros((30,1)), np.zeros((30,1)), np.zeros((30,1)), np.zeros((30,1))
for i in range(0,L):
  #update wi
  w1 = P1_inv.dot(H1.transpose().dot(C).dot(y1) - r1 + rho*z)
  w2 = P2_inv.dot(H2.transpose().dot(C).dot(y2) - r2 + rho*z)
  w3 = P3_inv.dot(H3.transpose().dot(C).dot(y3) - r3 + rho*z)
  w4 = P4_inv.dot(H4.transpose().dot(C).dot(y4) - r4 + rho*z)
  w5 = P5_inv.dot(H5.transpose().dot(C5).dot(y5) - r5 + rho*z)

  #update z
  z = 5*((w1 + w2 + w3 + w4 + w5)*rho/5 + (r1 + r2 + r3 + r4 + r5)/5)/(lamda + 5*rho)

  #update ri
  r1 = r1 + rho*(w1 - z)
  r2 = r2 + rho*(w2 - z)
  r3 = r3 + rho*(w3 - z)
  r4 = r4 + rho*(w4 - z)
  r5 = r5 + rho*(w5 - z)

y1_hat, y2_hat, y3_hat, y4_hat, y5_hat = np.zeros((114,1)), np.zeros((114,1)), np.zeros((114,1)), np.zeros((114,1)), np.zeros((113,1)),

for i in range(len(H1)):
  if H1.dot(z)[i] > 1.5:
    y1_hat[i] = 2
  else:
    y1_hat[i] = 1

for i in range(len(H2)):
  if H2.dot(z)[i] > 1.5:
    y2_hat[i] = 2
  else:
    y2_hat[i] = 1

for i in range(len(H3)):
  if H3.dot(z)[i] > 1.5:
    y3_hat[i] = 2
  else:
    y3_hat[i] = 1

for i in range(len(H4)):
  if H4.dot(z)[i] > 1.5:
    y4_hat[i] = 2
  else:
    y4_hat[i] = 1

for i in range(len(H5)):
  if H5.dot(z)[i] > 1.5:
    y5_hat[i] = 2
  else:
    y5_hat[i] = 1

error1 = np.linalg.norm(y1_hat-ry1, 1)

error2 = np.linalg.norm(y2_hat-ry2, 1)

error3 = np.linalg.norm(y3_hat-ry3, 1)

error4 = np.linalg.norm(y4_hat-ry4, 1)

error5 = np.linalg.norm(y5_hat-ry5, 1)

error_rate = 100*(error1 + error2 + error3 + error4 + error5)/669
error_rate