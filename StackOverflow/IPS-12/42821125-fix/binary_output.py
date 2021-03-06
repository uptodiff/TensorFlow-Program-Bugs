import tensorflow as tf
import random
import numpy as np

assert tf.__version__ == "1.8.0"
tf.set_random_seed(20180130)
np.random.seed(20180130)
random.seed(20180130)

X = tf.placeholder(tf.float32, shape=[None, 14], name='X')
Y = tf.placeholder(tf.float32, shape=[None, 1], name='Y')

W1 = tf.Variable(tf.truncated_normal(shape=[14, 20], stddev=0.5))
b1 = tf.Variable(tf.zeros([20]))
l1 = tf.nn.relu(tf.matmul(X, W1) + b1)

l1 = tf.nn.dropout(l1, 0.5)

W2 = tf.Variable(tf.truncated_normal(shape=[20, 20], stddev=0.5))
b2 = tf.Variable(tf.zeros([20]))
l2 = tf.nn.relu(tf.matmul(l1, W2) + b2)

l2 = tf.nn.dropout(l2, 0.5)

W3 = tf.Variable(tf.truncated_normal(shape=[20, 15], stddev=0.5))
b3 = tf.Variable(tf.zeros([15]))
l3 = tf.nn.relu(tf.matmul(l2, W3) + b3)

l3 = tf.nn.dropout(l3, 0.5)

W5 = tf.Variable(tf.truncated_normal(shape=[15, 1], stddev=0.5))
b5 = tf.Variable(tf.zeros([1]))
Yhat = tf.matmul(l3, W5) + b5
Ypred = tf.nn.sigmoid(Yhat)

loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=Yhat, labels=Y))

learning_rate = 0.005
l2_weight = 0.001
learner = tf.train.AdamOptimizer(learning_rate).minimize(loss)

correct_prediction = tf.equal(tf.greater(Y, 0.5), tf.greater(Ypred, 0.5))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

unit_train_inputX = []
unit_train_inputY = []
for i in range(100):
    unit_train_inputX.append(np.random.normal(0, 0.1, 14))
    if random.uniform(0, 3) > 1:
        unit_train_inputY.append([0])
        unit_train_inputX[-1] += random.randint(-1, 1)
    else:
        unit_train_inputY.append([1])

sess = tf.Session()
sess.run(tf.global_variables_initializer())
for i in range(100):
    _, loss_, accuracy_ = sess.run([learner, loss, accuracy],
                                   feed_dict={X: unit_train_inputX, Y: unit_train_inputY})

    print("loss {0}, accuracy {1}".format(loss_, accuracy_))
