## Install Fresh Ubuntu 22.04 in WSL2

1.  **Remove old WSL** (if needed):

    ```


    `wsl --unregister <DistroName>
    `

    ```

2.  **Install Ubuntu 22.04** from the Microsoft Store or via:

    ```


    `wsl --install -d Ubuntu-22.04
    `

    ```

3.  **Launch Ubuntu**, create a new user/pass.

---

## 2\. Update & Install Basics

1.  In Ubuntu:

    ```


    `sudo apt-get update
    sudo apt-get upgrade -y
    sudo apt-get install -y build-essential git curl wget python3 python3-dev python3-pip python3-venv
    `

    ```

---

## 3\. Install CUDA 11.8

1.  **Download** the `.deb` for Ubuntu 22.04 from [NVIDIA's CUDA Downloads](https://developer.nvidia.com/cuda-downloads). Example:

    ```


    `wget https://developer.download.nvidia.com/compute/cuda/11.8.0/local_installers/\
    `

    ```

cuda-repo-ubuntu2204-11-8-local_11.8.0-520.61.05-1_amd64.deb

````


`2. **Install**:
```bash
sudo dpkg -i cuda-repo-ubuntu2204-11-8-local_11.8.0-520.61.05-1_amd64.deb
sudo cp /var/cuda-repo-ubuntu2204-11-8-local/*.gpg /usr/share/keyrings/
sudo apt-get update
sudo apt-get -y install cuda-11-8
`

````

3.  **Update paths**:

    ```


    `echo 'export PATH=/usr/local/cuda-11.8/bin:$PATH' >> ~/.bashrc
    echo 'export LD_LIBRARY_PATH=/usr/local/cuda-11.8/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc
    source ~/.bashrc
    `

    ```

4.  **Verify**:

    ```


    `nvcc --version
    nvidia-smi
    `

    ```

---

## 4\. Install cuDNN 8

1.  Download **cuDNN v8** for **CUDA 11.x** from [NVIDIA's cuDNN page](https://developer.nvidia.com/cudnn).
2.  Extract, then copy the files:

    ```


    `tar -xvf cudnn-linux-x86_64-8.x.x.x_cuda11-archive.tar.xz
    cd cudnn-linux-x86_64-8.x.x.x_cuda11-archive
    sudo cp include/* /usr/local/cuda-11.8/include/
    sudo cp lib/* /usr/local/cuda-11.8/lib64/
    `

    ```

---

## 5\. Create a Virtual Environment & Install TensorFlow

1.  **Create** and **activate**:

    ```


    `python3 -m venv tf_gpu_env
    source tf_gpu_env/bin/activate
    `

    ```

2.  **Install TF**:

    ```


    `pip install --upgrade pip setuptools wheel
    pip install --upgrade tensorflow==2.14.*
    `

    ```

    _(2.14 or 2.13 typically aligns with CUDA 11.8 + cuDNN 8)_

---

## 6\. Verify GPU Detection

```


`python -c "import tensorflow as tf;
print(tf.config.list_physical_devices('GPU'));
print(tf.sysconfig.get_build_info())"
`

```

- Expect to see `[PhysicalDevice(name='/physical_device:GPU:0', ...)]` and `is_cuda_build: True`.

---

## Common Warnings (Safe to Ignore)

- **cuDNN/cuBLAS plugin registration** warnings.
- **NUMA node** warnings in WSL.
- **TensorRT** missing if you haven't installed it.

---

### That's It!

Following these steps ensures you have **matching versions** of CUDA, cuDNN, and TensorFlow for a successful GPU-accelerated setup in WSL2 Ubuntu 22.04.
