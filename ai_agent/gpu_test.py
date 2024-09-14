import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
print(tf.config.list_physical_devices())
print(tf.test.is_built_with_cuda())
print("t")