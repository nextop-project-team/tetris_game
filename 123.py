import tensorflow as tf
import numpy as np

xy = np.loadtxt('1.csv', delimiter=',', dtype=np.float32)
x_data = xy[:,:-1]
y_data = xy[:,[-1]] #x좌표
z_data = xy[:,[-2]] #회전수
print(len(x_data[0]))
print(z_data)


X = tf.placeholder(tf.float32, [None, 222])
Y = tf.placeholder(tf.float32, [None, 1])  # 0 ~ 6
Z = tf.placeholder(tf.float32, [None, 1])


W = tf.Variable(tf.random_normal([222,1]), name='weight1')
b = tf.Variable(tf.random_normal([1]), name='bias')
z = tf.Variable(tf.random_normal([1]), name='bbb')

hypothesis = tf.matmul(X, W) + b #x좌표가설
hypoth = tf.matmul(X,W) + z #회전수가설

cost = tf.reduce_mean(tf.square(hypothesis - Y))
cost1 = tf.reduce_mean(tf.square(hypoth - Z)) #회전수

        # Minimize
optimizer = tf.train.GradientDescentOptimizer(learning_rate=1e-5)

train = optimizer.minimize(cost)
train1 = optimizer.minimize(cost1)

        # Launch the graph in a session.
sess = tf.Session()
        # Initializes global variables in the graph.
sess.run(tf.global_variables_initializer())

for step in range(2000001):
    cost_val, hy_val, _ = sess.run(
        [cost, hypothesis, train], feed_dict={X: x_data, Y: y_data})
    cost_val1, hy_val1, _ = sess.run(
        [cost1, hypoth, train1], feed_dict={X: x_data, Z: z_data})
    if step % 6000 == 0:
        print(step, "Cost: ", cost_val, "\nPrediction: X,cordi\n", hy_val)
        print(step, "Cost: ", cost_val1, "\nPrediction: turn\n", hy_val1)

'''
for step in range(200001):
    cost_val1, hy_val1, _ = sess.run(
        [cost1, hypoth, train1], feed_dict={X: x_data, Z: z_data})
    if step % 2000 == 0:
        print(step, "Cost: ", cost_val1, "\nPrediction: turn\n", hy_val1)
'''