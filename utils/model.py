from tensorflow.keras.models import *
from tensorflow.keras.layers import *
from tensorflow.keras.optimizers import *

def u_net(pretrained_weights=None, input_size=(256, 256, 1), start_neurons=64):
    
    """
    :param pretrained_weights: 预训练的模型参数
    :param input_size: 模型输入图像尺寸，这里是256x256的灰度图像，因此第三个元素值为1
    :param start_neurons: 神经元个数
    :return: U-Net网络模型
    """
    
    # 输入层
    inputs = Input(input_size)
    
    # 第一层（卷积两次池化一次）
    conv1 = Conv2D(start_neurons * 1, 3, activation='relu', padding='same', kernel_initializer='he_normal')(inputs)
    conv1 = BatchNormalization()(conv1)
    conv1 = Conv2D(start_neurons * 1, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv1)
    pool1 = MaxPooling2D(pool_size=(2, 2))(conv1)
    pool1 = Dropout(0.25)(pool1)
    
    # 第二层（卷积两次池化一次）
    conv2 = Conv2D(start_neurons * 2, 3, activation='relu', padding='same', kernel_initializer='he_normal')(pool1)
    conv2 = BatchNormalization()(conv2)
    conv2 = Conv2D(start_neurons * 2, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv2)
    pool2 = MaxPooling2D(pool_size=(2, 2))(conv2)
    pool2 = Dropout(0.5)(pool2)
    
    # 第三层（卷积两次池化一次）
    conv3 = Conv2D(start_neurons * 4, 3, activation='relu', padding='same', kernel_initializer='he_normal')(pool2)
    conv3 = BatchNormalization()(conv3)
    conv3 = Conv2D(start_neurons * 4, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv3)
    pool3 = MaxPooling2D(pool_size=(2, 2))(conv3)
    pool3 = Dropout(0.5)(pool3)
    
    # 第四层（卷积两次池化一次）
    conv4 = Conv2D(start_neurons * 8, 3, activation='relu', padding='same', kernel_initializer='he_normal')(pool3)
    conv4 = BatchNormalization()(conv4)
    conv4 = Conv2D(start_neurons * 8, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv4)
    pool4 = MaxPooling2D(pool_size=(2, 2))(conv4)
    pool4 = Dropout(0.5)(pool4)
    
    # 第五层，降采样完成，准备升采样
    conv5 = Conv2D(start_neurons * 16, 3, activation='relu', padding='same', kernel_initializer='he_normal')(pool4)
    conv5 = BatchNormalization()(conv5)
    conv5 = Conv2D(start_neurons * 16, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv5)
    
    # 第四层，反卷积
    deconv4 = Conv2DTranspose(start_neurons * 8, 3, strides=(2, 2), activation='relu', padding='same',
                              kernel_initializer='he_normal')(conv5)
    uconv4 = concatenate([conv4, deconv4])
    uconv4 = Dropout(0.5)(uconv4)
    uconv4 = Conv2D(start_neurons * 8, 3, activation='relu', padding='same', kernel_initializer='he_normal')(uconv4)
    uconv4 = BatchNormalization()(uconv4)
    uconv4 = Conv2D(start_neurons * 8, 3, activation='relu', padding='same', kernel_initializer='he_normal')(uconv4)
    
    # 第三层，反卷积
    deconv3 = Conv2DTranspose(start_neurons * 4, 3, strides=(2, 2), activation='relu', padding='same',
                              kernel_initializer='he_normal')(uconv4)
    uconv3 = concatenate([conv3, deconv3])
    uconv3 = Dropout(0.5)(uconv3)
    uconv3 = Conv2D(start_neurons * 4, 3, activation='relu', padding='same', kernel_initializer='he_normal')(uconv3)
    uconv3 = BatchNormalization()(uconv3)
    uconv3 = Conv2D(start_neurons * 4, 3, activation='relu', padding='same', kernel_initializer='he_normal')(uconv3)
    
    # 第二层，反卷积
    deconv2 = Conv2DTranspose(start_neurons * 2, 3, strides=(2, 2), activation='relu', padding='same',
                              kernel_initializer='he_normal')(uconv3)
    uconv2 = concatenate([conv2, deconv2])
    uconv2 = Dropout(0.5)(uconv2)
    uconv2 = Conv2D(start_neurons * 2, 3, activation='relu', padding='same', kernel_initializer='he_normal')(uconv2)
    uconv2 = BatchNormalization()(uconv2)
    uconv2 = Conv2D(start_neurons * 2, 3, activation='relu', padding='same', kernel_initializer='he_normal')(uconv2)
   
    # 第一层反卷积
    deconv1 = Conv2DTranspose(start_neurons * 1, 3, strides=(2, 2), activation='relu', padding='same',
                              kernel_initializer='he_normal')(uconv2)
    uconv1 = concatenate([conv1, deconv1])
    uconv1 = Dropout(0.5)(uconv1)
    uconv1 = Conv2D(start_neurons * 1, 3, activation='relu', padding='same', kernel_initializer='he_normal')(uconv1)
    uconv1 = BatchNormalization()(uconv1)
    uconv1 = Conv2D(start_neurons * 1, 3, activation='relu', padding='same', kernel_initializer='he_normal')(uconv1)
    
    # 1 x 1卷积，输出层
    outputs = Conv2D(1, 1, padding='same', activation='sigmoid')(uconv1)
    
    # 联合输入和输出构建模型
    model = Model(inputs, outputs)
    
    # 设置模型的优化器、损失函数和度量标准
    model.compile(optimizer=Adam(lr=1e-4), loss='binary_crossentropy', metrics=['accuracy'])
    
    # 输出模型概述信息
    print("模型概述信息如下：")
    model.summary()
    
    # 是否使用预训练的参数
    if pretrained_weights:
        model.load_weights(pretrained_weights)

    return model
