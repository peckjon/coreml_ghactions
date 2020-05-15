import numpy as np
import pycuda.autoinit
import pycuda.gpuarray as gpuarray

a = np.array([1, 2, 3, 4, 5]).astype(np.float32)
a_gpu = gpuarray.to_gpu(a)
result = pow(a_gpu, a_gpu).get()
print(result)
