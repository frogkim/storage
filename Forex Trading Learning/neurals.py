import tensorflow.compat.v1 as tf

tf.disable_v2_behavior()
from datetime import datetime


class NUERALS:
    def __init__(self, session, name):
        # setting for neural net
        self.session = session
        self.net_name = name
        self.learning_sample_lines = 20  # learning sample lines

        self.input_size = 120
        self.output_size = 3
        self.neural_size = 128
        self.l_rate = 1e-3
        self.activation = tf.nn.relu
        self.optimizer = tf.train.RMSPropOptimizer(learning_rate=self.l_rate)

        with tf.variable_scope(self.net_name + "placeholders"):
            # placeholder X and Y
            self._x = tf.placeholder(tf.float32, [None, self.learning_sample_lines, self.input_size], name="input_x")
            self._y = tf.placeholder(tf.float32, [None, 1, self.output_size], name="input_y")
            self._balance = tf.placeholder(tf.float32, name="Balance")

        with tf.variable_scope(self.net_name + "LSTM"):
            convert_i = self._CreateVariable("_convert_", 0, self.input_size, self.neural_size)
            convert_o = self._CreateVariable("_convert_", 1, self.neural_size, self.output_size)
            short = self._CreateVariable("_short_", 0, 1, self.neural_size)
            long = self._CreateVariable("_long_", 0, 1, self.neural_size)
            w_list = [self._CreateVariable("_weight_", i, self.neural_size, self.neural_size) for i in range(8)]
            b_list = [self._CreateBias("_bias_", i, self.neural_size) for i in range(4)]

        train_list = [convert_i, convert_o] + w_list + b_list
        self.copy_list = [convert_i, convert_o, short, long] + w_list + b_list

        for i in range(self.learning_sample_lines):
            i_data = tf.matmul(self._x[:, i, :], convert_i)
            o_data, short, long = self._LSTM(i_data, short, long, w_list, b_list)

        with tf.variable_scope(self.net_name + "Pred"):
            self.pred = tf.matmul(o_data, convert_o)
            self.loss = tf.reduce_sum(tf.square(self._y - self.pred))
            grads_and_vars = self.optimizer.compute_gradients(self.loss, train_list)
            self.train = self.optimizer.apply_gradients(grads_and_vars)

        now = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        root_logdir = "tf_logs"
        logdir = "{}/run-{}/".format(root_logdir, now)
        self.mse_summary = tf.summary.scalar('MSE', self.loss)
        self.bal_summary = tf.summary.scalar('BALANCE', self._balance)
        self.file_writer = tf.summary.FileWriter(logdir, tf.get_default_graph())

    # build network    # predict

    def StoreGraph(self, summary_str, balance_str, step):
        self.file_writer.add_summary(summary_str, step)
        self.file_writer.add_summary(balance_str, int(step/200))

    def GraphClose(self):
        self.file_writer.close()

    def Predict(self, x_stack):
        return self.session.run(self.pred, feed_dict={self._x: x_stack})

    # learning
    def Update(self, x_stack, y_stack, balance):
        return self.session.run([self.loss, self.train, self.mse_summary, self.bal_summary],
                                feed_dict={self._x: x_stack, self._y: y_stack, self._balance: balance})

    def CopyOps(self, other):
        self._Copy_op = [self.copy_list[i].assign(other.copy_list[i]) for i in range(len(self.copy_list))]

    def Copy(self):
        self.session.run(self._Copy_op)

    def _CreateVariable(self, name, number, i_size, o_size):
        weight_name = self.net_name + name + str(number)
        return tf.get_variable(weight_name,
                               shape=[i_size, o_size],
                               initializer=tf.keras.initializers.glorot_uniform())

    def _CreateBias(self, name, number, o_size):
        bias_name = self.net_name + name + "_bias_" + str(number)
        return tf.get_variable(bias_name,
                               shape=[1, o_size],
                               initializer=tf.keras.initializers.glorot_uniform())

    def _LSTM(self, i_data, short, long, w_list, b_list):
        i_t = tf.matmul(i_data, w_list[0]) + tf.matmul(short, w_list[1]) + b_list[0]
        i_t = tf.nn.sigmoid(i_t)
        f_t = tf.matmul(i_data, w_list[2]) + tf.matmul(short, w_list[3]) + b_list[1]
        f_t = tf.nn.sigmoid(f_t)
        o_t = tf.matmul(i_data, w_list[4]) + tf.matmul(short, w_list[5]) + b_list[2]
        o_t = tf.nn.sigmoid(o_t)
        g_t = tf.matmul(i_data, w_list[6]) + tf.matmul(short, w_list[7]) + b_list[3]
        g_t = tf.nn.tanh(g_t)

        long = f_t * long + i_t * g_t
        short = o_t * tf.nn.tanh(long)
        o_data = short
        return o_data, short, long
