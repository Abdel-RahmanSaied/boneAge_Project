from keras.applications.vgg16 import VGG16
from keras.layers import GlobalAveragePooling2D, Dense, Dropout, Flatten, Input, Conv2D, multiply, LocallyConnected2D, \
    Lambda
from keras.models import Model
from keras.layers import BatchNormalization
import numpy as np
from keras.metrics import mean_absolute_error
import os


def model_weights():
    # t_x = np.zeros((10, 224, 224, 3))
    t_x = (384, 384, 3)

    in_lay = Input(t_x)
    base_pretrained_model = VGG16(input_shape=t_x, include_top=False, weights='imagenet')
    base_pretrained_model.trainable = False

    # Call VGG16 with the input layer to define its output shape
    pt_features = base_pretrained_model(in_lay)

    bn_features = BatchNormalization()(pt_features)

    # here we do an attention mechanism to turn pixels in the GAP on an off
    attn_layer = Conv2D(64, kernel_size=(1, 1), padding='same', activation='relu')(bn_features)
    attn_layer = Conv2D(16, kernel_size=(1, 1), padding='same', activation='relu')(attn_layer)
    attn_layer = LocallyConnected2D(1, kernel_size=(1, 1), padding='valid', activation='sigmoid')(attn_layer)

    pt_features = base_pretrained_model(in_lay)
    pt_features = GlobalAveragePooling2D()(pt_features)

    pt_depth = pt_features.shape[-1]

    # fan it out to all of the channels
    up_c2_w = np.ones((1, 1, 1, pt_depth))
    up_c2 = Conv2D(pt_depth, kernel_size=(1, 1), padding='same', activation='linear', use_bias=False, weights=[up_c2_w])
    up_c2.trainable = False
    attn_layer = up_c2(attn_layer)

    mask_features = multiply([attn_layer, bn_features])
    gap_features = GlobalAveragePooling2D()(mask_features)
    gap_mask = GlobalAveragePooling2D()(attn_layer)

    # to account for missing values from the attention model
    gap = Lambda(lambda x: x[0] / x[1], name='RescaleGAP')([gap_features, gap_mask])
    gap_dr = Dropout(0.5)(gap)
    dr_steps = Dropout(0.25)(Dense(1024, activation='elu')(gap_dr))
    out_layer = Dense(1, activation='linear')(dr_steps)  # linear is what 16bit did
    bone_age_model = Model(inputs=[in_lay], outputs=[out_layer])

    return bone_age_model


def Aimodel():
    bone_age_model = model_weights()
    # AiModel/model/bone_age_weights.best.hdf5
    bone_age_model.load_weights(os.path.join(os.getcwd(), 'AiModel', 'model', 'bone_age_weights.best.hdf5'))
    return bone_age_model
