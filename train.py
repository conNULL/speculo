
import tensorflow as tf
import numpy
import json
import matplotlib.pyplot as plt
from get_data import Data
import operator

words = ['tech', 'apple', 'google', 'baidu', 'phone', 'internet', 'router', 'wifi', 'artificial', 'intelligence', 'machine', 'laptop', 'desktop', 'mac', 'automation','roomba','robot','microcontroller','software','hardware', 'engineering']
train_cities = ['Toronto', 'San Francisco', 'Boston', 'New York', 'Mexico City']
train_scores = [800, 1000, 900, 950, 400]
test, train = Data.get_data(words, train_cities,train_scores )

rng = numpy.random

# Parameters
learning_rate = 0.01
training_epochs = 1000
display_step = 50
train_X = []
train_Y = []
test_X = []
test_Y = []

f = open('cities.txt', 'r')
text = f.readlines()[0]
cities = text[1:-1].replace('\'', '').split(',')
f.close()

for key in train:
    train_X.append(numpy.asarray(train[key][:-1]))
    train_Y.append(numpy.asarray(train[key][-1:]))

train_X = numpy.asarray(train_X)
train_Y = numpy.asarray(train_Y)
# Training Data
# train_X = numpy.asarray([3.3,4.4,5.5,6.71,6.93,4.168,9.779,6.182,7.59,2.167,
#                          7.042,10.791,5.313,7.997,5.654,9.27,3.1])
# train_Y = numpy.asarray([1.7,2.76,2.09,3.19,1.694,1.573,3.366,2.596,2.53,1.221,
#                          2.827,3.465,1.65,2.904,2.42,2.94,1.3])
n_samples = train_X.shape[0]

# tf Graph Inumpyut
X = tf.placeholder("float")
Y = tf.placeholder("float")

# Set model weights
W = tf.Variable(rng.randn(), name="weight")
b = tf.Variable(rng.randn(), name="bias")

# Construct a linear model
pred = tf.add(numpy.dot(X, W), b)

# Mean squared error
cost = tf.reduce_sum(tf.pow(pred-Y, 2))/(2*n_samples)
# Gradient descent
#  Note, minimize() knows to modify W and b because Variable objects are trainable=True by default
optimizer = tf.train.AdamOptimizer(learning_rate).minimize(cost)

# Initialize the variables (i.e. assign their default value)
init = tf.global_variables_initializer()

# Start training
with tf.Session() as sess:

    # Run the initializer
    sess.run(init)

    # Fit all training data
    for epoch in range(training_epochs):
        for (x, y) in zip(train_X, train_Y):
            sess.run(optimizer, feed_dict={X: x, Y: y})

        # Display logs per epoch step
        if (epoch+1) % display_step == 0:
            c = sess.run(cost, feed_dict={X: train_X, Y:train_Y})
            print("Epoch:", '%04d' % (epoch+1), "cost=", "{:.9f}".format(c), \
                "W=", sess.run(W), "b=", sess.run(b))

    print("Optimization Finished!")
    training_cost = sess.run(cost, feed_dict={X: train_X, Y: train_Y})
    print("Training cost=", training_cost, "W=", sess.run(W), "b=", sess.run(b), '\n')

    for key in test:
        test_X.append(numpy.asarray(test[key][:-1]))
        test_Y.append(numpy.asarray(test[key][-1:]))
    
    scores = {}
    test_X = numpy.asarray(test_X)
    test_Y = numpy.asarray(test_Y)

    count = 0
    score = sess.run(pred, feed_dict={X: test_X, Y: test_Y})
    for i in range(len(cities)):
        if not cities[i] in train_cities:
            scores[cities[i]] = tf.reduce_sum(score[i-count]).name[4:].split(':')[0]
        else:
            count += 1
    print(scores)
    
    
    sorted_cities = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)
    f = open('scores.txt', 'w')
    json.dump(scores, f)
    f.close()
    
    f = open('best.txt', 'w')
    json.dump(sorted_cities[:10], f)
    f.close()
    
    print(sorted_cities[:10])