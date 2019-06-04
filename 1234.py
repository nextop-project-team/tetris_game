import tensorflow as tf
import numpy as np

xy = np.loadtxt('1.csv', delimiter=',', dtype=np.float32)
x_data = xy[:,:-1]
y_data = xy[:,[-1]] #x좌표
print(len(x_data[0]))



X = tf.placeholder(tf.float32, [None, 222])
Y = tf.placeholder(tf.int32, [None, 1])  # 0 ~ 6



W = tf.Variable(tf.random_normal([222,10]), name='weight1')
b = tf.Variable(tf.random_normal([10]), name='bias')

hypothesis = tf.matmul(X, W) + b


cost = tf.reduce_mean(tf.square(hypothesis - Y))

        # Minimize
optimizer = tf.train.GradientDescentOptimizer(learning_rate=1e-5)
train = optimizer.minimize(cost)
print("i")
        # Launch the graph in a session.
sess = tf.Session()
        # Initializes global variables in the graph.
sess.run(tf.global_variables_initializer())
for step in range(2001):
    cost_val, hy_val, _ = sess.run(
        [cost, hypothesis, train], feed_dict={X: x_data, Y: y_data})
    if step % 10 == 0:
        print(step, "Cost: ", cost_val, "\nPrediction:\n", hy_val)