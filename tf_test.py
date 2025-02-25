import os
import tensorflow as tf
print("TensorFlow version:", tf.__version__)
print("Is built with CUDA:", tf.test.is_built_with_cuda())
print("GPUs found:", tf.config.list_physical_devices('GPU'))
# os.environ["TF_CPP_MIN_LOG_LEVEL"] = "0"
# tf.debugging.set_log_device_placement(True)
# with tf.device('/GPU:0'):
#     a = tf.constant([1.0, 2.0])
#     b = tf.constant([3.0, 4.0])
#     print(a + b)
