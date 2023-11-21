from keras.models import Sequential
from keras.layers import Conv1D, MaxPooling1D, BatchNormalization
from keras.layers import Activation, Flatten, Dense, Dropout
from keras.layers import ELU
from keras.initializers import glorot_uniform

class DFNet:
    @staticmethod
    def build(input_shape, classes):
        model = Sequential()
        
        model.add(Dropout(0.1))
        model.add(Conv1D(filters=32, kernel_size=8, input_shape=input_shape,
                         strides=1, padding='same'))
        model.add(ELU(alpha=1.0))
        model.add(MaxPooling1D(pool_size=8, strides=4,
                               padding='same'))

        model.add(Conv1D(filters=64, kernel_size=8,
                         strides=1, padding='same'))
        model.add(Activation('relu'))
        model.add(MaxPooling1D(pool_size=8, strides=4,
                               padding='same'))
        
        model.add(Conv1D(filters=128, kernel_size=8,
                         strides=1, padding='same'))
        model.add(Activation('relu'))
        model.add(MaxPooling1D(pool_size=8, strides=4,
                               padding='same'))

        model.add(Flatten())
        model.add(Dense(512, kernel_initializer=glorot_uniform(seed=0)))
        model.add(BatchNormalization())
        model.add(Activation('relu'))

        model.add(Dropout(0.7))

        model.add(Dense(512, kernel_initializer=glorot_uniform(seed=0)))
        model.add(BatchNormalization())
        model.add(Activation('relu'))

        model.add(Dropout(0.5))

        model.add(Dense(classes, kernel_initializer=glorot_uniform(seed=0)))
        model.add(Activation('softmax'))
        return model