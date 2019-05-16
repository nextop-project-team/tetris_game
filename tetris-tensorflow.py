import tensorflow as tf
import numpy as np



xy = np.loadtxt('데이터 입력받기', delimiter=',', dtype=np.float32)
inputshape_data = xy[0] #x1
inputboard_data = xy[:, 1: ] # 0에는 블럭모양 나머지는 보드값 --입력값,x2
y_data = xy[] #y데이터에 뭘 넣어야할지

x1 = tf.placeholder(tf.float32)
x2 = tf.placeholder(tf.float32)

Y = tf.placeholder(tf.float32)

w1 = tf.Variable(tf.random_normal([1]), name='weight1')
w2 = tf.Variable(tf.random_normal([1]), name='weight2')

b = tf.Variable(tf.random_normal([1]), name='bias')

hypothesis = x1 * w1 + x2 * w2  + b #가설 = 움직일x값

cost = tf.reduce_mean(tf.square(hypothesis - Y)) #손실함수

optimizer = tf.train.GradientDescentOptimizer(learning_rate=1e-5) #경사하강
train = optimizer.minimize(cost)

sess = tf.Session()

sess.run(tf.global_variables_initializer())



rotate_data = [] #회전수
movex_data = [] #움직일 x좌표

