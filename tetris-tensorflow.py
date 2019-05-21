import tensorflow as tf
import numpy as np



xy = np.loadtxt('1.csv', delimiter=',', dtype=np.float32)
inputshape_data = xy[0] #입력 블럭모양
inputboard_data = xy[0:220] #보드데이터
y_data = xy[220:222]  #y데이터에 뭘 넣어야할지


#outputmovex_data= xy[] #출력 x움직임
#outputrotate_data = xy[] #출력회전수
#rotate_data = [] #회전수
#movex_data = [] #움직일 x좌표
print(inputboard_data)
print(y_data)

x1 = tf.placeholder(tf.float32)
x2 = tf.placeholder(tf.float32)
xy = tf.placeholder(tf.float32)


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

for step in range(2001):
    cost_val, hy_val, _ = sess.run([cost, hypothesis, train],
                                    feed_dict={x1: inputboard_data, x2: inputshape_data, Y: y_data})
    if step % 10 == 0:
        print(step, "Cost: ", cost_val, "\nPrediction:\n", hy_val)