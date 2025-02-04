# -*- coding: utf-8 -*-
# @Project:AID1810
# @Author:biabu
# @Date:2019/4/20 15:19
# @File_name:dcgan.py
# @IDE:PyCharm

"""反卷积对抗生成网络， DCGAN 分析 mnist"""

import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.examples.tutorials.mnist import input_data


class Dcgan():
    def __init__(self):
        self.mnist = input_data.read_data_sets('./data/mnist')

    # 获取数据
    def get_inputs(self, noise_dim, image_height, image_width, image_depth):
        inputs_real = tf.placeholder(tf.float32, [None, image_height, image_width, image_depth], name='inputs_real')
        inputs_noise = tf.placeholder(tf.float32, [None, noise_dim], name='inputs_noise')
        return inputs_real, inputs_noise

    # 生成器
    def get_generator(self, noise_dim, output_dim, is_train=True, alpha=0.01):
        with tf.variable_scope('generator', reuse=(not is_train)):
            # 100*1 -> 4*4*512
            # 全连接层
            layer1 = tf.layers.dense(noise_dim, 4*4*512)
            layer1 = tf.reshape(layer1, [-1, 4, 4, 512])
            # Batch Normalization 批标准化
            layer1 = tf.layers.batch_normalization(layer1, training=is_train)
            # Leaky ReLU
            layer1 = tf.maximum(alpha*layer1, layer1)
            # dropout
            layer1 = tf.nn.dropout(layer1, keep_prob=0.8)

            # 4 x 4 x 512 to 7 x 7 x 256, 反卷积
            # padding = valid = 0
            # h = (w - 1) * s - p + f = 3 + 4
            layer2 = tf.layers.conv2d_transpose(layer1, filters=256, kernel_size=4, strides=1, padding='valid')
            layer2 = tf.layers.batch_normalization(layer2, training=is_train)
            layer2 = tf.maximum(alpha * layer2, layer2)
            layer2 = tf.nn.dropout(layer2, keep_prob=0.8)

            # 7 x 7 256 to 14 x 14 x 128
            # padding = same = 1
            # h = (w - 1) * s - 2p + f = 6*2 - 1 + 3 = 14
            layer3 = tf.layers.conv2d_transpose(layer2, 128, 3, strides=2, padding='same')
            layer3 = tf.layers.batch_normalization(layer3, training=is_train)
            layer3 = tf.maximum(alpha * layer3, layer3)
            layer3 = tf.nn.dropout(layer3, keep_prob=0.8)

            # 14 x 14 x 128 to 28 x 28 x 1
            logits = tf.layers.conv2d_transpose(layer3, output_dim, 3, strides=2, padding='same')
            # MNIST原始数据集的像素范围在0-1，这里的生成图片范围为(-1,1)
            # 因此在训练时，记住要把MNIST像素范围进行resize
            outputs = tf.tanh(logits)

            return outputs

    # 判别器
    def get_discriminator(self, inputs_img, reuse=False, alpha=0.01):
        with tf.variable_scope("discriminator", reuse=reuse):
            # 28 x 28 x 1 to 14 x 14 x 128
            # h = w = (28 - 3 + 1) / 2 + 1 = 14
            # 第一层不加入BN
            layer1 = tf.layers.conv2d(inputs_img, 128, 3, strides=2, padding='same')
            layer1 = tf.maximum(alpha * layer1, layer1)
            layer1 = tf.nn.dropout(layer1, keep_prob=0.8)

            # 14 x 14 x 128 to 7 x 7 x 256
            layer2 = tf.layers.conv2d(layer1, 256, 3, strides=2, padding='same')
            layer2 = tf.layers.batch_normalization(layer2, training=True)
            layer2 = tf.maximum(alpha * layer2, layer2)
            layer2 = tf.nn.dropout(layer2, keep_prob=0.8)

            # 7 x 7 x 256 to 4 x 4 x 512
            layer3 = tf.layers.conv2d(layer2, 512, 3, strides=2, padding='same')
            layer3 = tf.layers.batch_normalization(layer3, training=True)
            layer3 = tf.maximum(alpha * layer3, layer3)
            layer3 = tf.nn.dropout(layer3, keep_prob=0.8)

            # 4 x 4 x 512 to 4*4*512 x 1
            flatten = tf.reshape(layer3, (-1, 4 * 4 * 512))
            logits = tf.layers.dense(flatten, 1)
            outputs = tf.sigmoid(logits)

            return logits, outputs

    # 损失函数
    def get_loss(self, inputs_real, inputs_noise, image_depth, smooth=0.1):
        g_outputs = self.get_generator(inputs_noise, image_depth, is_train=True)
        d_logits_real, d_outputs_real = self.get_discriminator(inputs_real)
        d_logits_fake, d_outputs_fake = self.get_discriminator(g_outputs, reuse=True)

        # 计算Loss
        g_loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=d_logits_fake, labels=tf.ones_like(d_outputs_fake) * ( - smooth)))
        d_loss_real = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=d_logits_real, labels=tf.ones_like(d_outputs_real) * ( 1 - smooth)))
        d_loss_fake = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=d_logits_fake, labels=tf.zeros_like(d_outputs_fake)))
        d_loss = tf.add(d_loss_real, d_loss_fake)

        return g_loss, d_loss

    # 损失函数优化
    def get_optimizer(self, g_loss, d_loss, beta1=0.4, learning_rate=0.001):
        train_vars = tf.trainable_variables()

        g_vars = [var for var in train_vars if var.name.startswith("generator")]
        d_vars = [var for var in train_vars if var.name.startswith("discriminator")]

        # Optimizer
        with tf.control_dependencies(tf.get_collection(tf.GraphKeys.UPDATE_OPS)):
            g_opt = tf.train.AdamOptimizer(learning_rate).minimize(g_loss, var_list=g_vars)
            d_opt = tf.train.AdamOptimizer(learning_rate).minimize(d_loss, var_list=d_vars)

        return g_opt, d_opt

    # 打印图像
    def plot_images(self,samples):
        fig, axes = plt.subplots(nrows=1, ncols=25, sharex=True, sharey=True, figsize=(50, 2))
        for img, ax in zip(samples, axes):
            ax.imshow(img.reshape((28, 28)), cmap='Greys_r')
            ax.get_xaxis().set_visible(False)
            ax.get_yaxis().set_visible(False)
        fig.tight_layout(pad=0)

    # 打印生成的图像
    def show_generator_output(self, sess, n_images, inputs_noise, output_dim):
        cmap = 'Greys_r'
        noise_shape = inputs_noise.get_shape().as_list()[-1]
        # 生成噪声图片
        examples_noise = np.random.uniform(-1, 1, size=[n_images, noise_shape])
        samples = sess.run(self.get_generator(inputs_noise, output_dim, False),feed_dict={inputs_noise: examples_noise})
        result = np.squeeze(samples, -1)
        return result

    # 训练模型
    def train(self, noise_size, data_shape, batch_size, n_samples, epochs, learning_rate=0.01, beta1=0.4):
        # 存储loss
        losses = []
        steps = 0
        # 获取数据格式，初始化
        inputs_real, inputs_noise = self.get_inputs(noise_size, data_shape[1], data_shape[2], data_shape[3])
        # 获取损失
        g_loss, d_loss = self.get_loss(inputs_real, inputs_noise, data_shape[-1])
        # 进行损失优化
        g_train_opt, d_train_opt = self.get_optimizer(g_loss, d_loss, beta1, learning_rate)

        # 开启会话，进行训练
        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())
            # 迭代epoch
            for e in range(epochs):
                for batch_i in range(self.mnist.train.num_examples // batch_size):
                    steps += 1
                    batch = self.mnist.train.next_batch(batch_size)

                    batch_images = batch[0].reshape((batch_size, data_shape[1], data_shape[2], data_shape[3]))
                    # scale to -1, 1
                    batch_images = batch_images * 2 - 1

                    # noise
                    batch_noise = np.random.uniform(-1, 1, size=(batch_size, noise_size))

                    # run optimizer
                    _ = sess.run(g_train_opt, feed_dict={inputs_real: batch_images,
                                                         inputs_noise: batch_noise})
                    _ = sess.run(d_train_opt, feed_dict={inputs_real: batch_images,
                                                         inputs_noise: batch_noise})

                    if steps % 101 == 0:
                        train_loss_d = d_loss.eval({inputs_real: batch_images,
                                                    inputs_noise: batch_noise})
                        train_loss_g = g_loss.eval({inputs_real: batch_images,
                                                    inputs_noise: batch_noise})
                        losses.append((train_loss_d, train_loss_g))
                        # 显示图片
                        samples = self.show_generator_output(sess, n_samples, inputs_noise, data_shape[-1])
                        self.plot_images(samples)
                        print("Epoch {}/{}....".format(e + 1, epochs),
                              "Discriminator Loss: {:.4f}....".format(train_loss_d),
                              "Generator Loss: {:.4f}....".format(train_loss_g))


if __name__ == '__main__':
    batch_size = 64
    noise_size = 100
    epochs = 5
    n_samples = 25
    dcgan = Dcgan()
    with tf.Graph().as_default():
        dcgan.train(noise_size, [-1, 28, 28, 1], batch_size, n_samples, epochs)
