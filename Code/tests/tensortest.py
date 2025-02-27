import tensorflow as tf

# Create a simple matrix on the GPU
with tf.device('/GPU:0'):
    x = tf.random.normal((1000, 1000))
    y = tf.linalg.matmul(x, x)

print("Result shape:", y.shape)
print("Is GPU used?", y.device)
