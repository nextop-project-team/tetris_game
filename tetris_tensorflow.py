import tensorflow as tf
import numpy as np


class ai:
    def train(self):
        xy = np.loadtxt('1.csv', delimiter=',', dtype=np.float32)
        x_data = xy[:,:-1]
        y_data = xy[:,[-1]] #회전 수
        print(len(x_data[0]))

        #outputmovex_data= xy[] #출력 x움직임
        #outputrotate_data = xy[] #출력회전수
        #rotate_data = [] #회전수
        #movex_data = [] #움직일 x좌표
        #print(inputshape_data)
        #print(inputboard_data)
        # print(x_data)
        # print(y_data)


        X = tf.placeholder(tf.float32, [None, 222])
        Y = tf.placeholder(tf.int32, [None, 1])  # 0 ~ 6

        Y_one_hot = tf.one_hot(Y, 1)  # one hot
        print("one_hot:", Y_one_hot)
        Y_one_hot = tf.reshape(Y_one_hot, [-1, 10])
        print("reshape one_hot:", Y_one_hot)


        W = tf.Variable(tf.random_normal([222,10]), name='weight1')
        b = tf.Variable(tf.random_normal([10]), name='bias')

        logits = tf.matmul(X, W) + b
        hypothesis = tf.nn.softmax(logits)

        sess = tf.Session()
        sess.run(tf.global_variables_initializer())
        print(sess.run(hypothesis,feed_dict={X: x_data}))

        # Cross entropy cost/loss
        cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(logits=logits,
                                                                         labels=tf.stop_gradient([Y_one_hot])))
        optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.1).minimize(cost)

        prediction = tf.argmax(hypothesis, 1)
        correct_prediction = tf.equal(prediction, tf.argmax(Y_one_hot, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

        # Launch graph
        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())

            for step in range(2001):
                _, cost_val, acc_val = sess.run([optimizer, cost, accuracy], feed_dict={X: x_data, Y: y_data})

                if step % 100 == 0:
                    print("Step: {:5}\tCost: {:.3f}\tAcc: {:.2%}".format(step, cost_val, acc_val))

            # Let's see if we can predict
            pred = sess.run(prediction, feed_dict={X: x_data})
            # y_data: (N,1) = flatten => (N, ) matches pred.shape
            for p, y in zip(pred, y_data.flatten()):
                print("[{}] Prediction: {} True Y: {}".format(p == int(y), p, int(y)))
            ai[3]=(0,p,0)
        return ai

AI = ai()