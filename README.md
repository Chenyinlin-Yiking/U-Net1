# U-Net医学图像分割

# 代码介绍
代码是论文 "[U-Net: Convolutional Networks for Biomedical Image Segmentation](https://link.springer.com/chapter/10.1007%2F978-3-319-24574-4_28)" 的 Python 实现。 本代码是基于 [unet](https://github.com/zhixuhao/unet) 的改进，主要是把代码从 TensorFlow 1 升级到 TensorFlow 2，并实现多GPU训练策略，同时增加代码的中文注释。

# 代码使用方法
1. git clone https://github.com/xujinzh/U-Net.git
2. python main.py --train ./data/membrane/train --test ./data/membrane/test --steps 100 --epochs 25

数据使用的是 [ISBI Challenge: Segmentation of neuronal structures in EM stacks
](http://brainiac2.mit.edu/isbi_challenge/).

# 依赖包
- python3
- tensorflow2
- numpy
- skimage
