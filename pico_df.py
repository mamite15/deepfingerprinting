import pickle
import numpy as np
import keras
from keras import backend as K
from pico_df_model import DFNet
from keras.optimizers import Adamax

def main():
    print("DFモデルの学習と評価開始")

    NB_EPOCH=30
    BATCH_SIZE=128
    VERBOSE=2
    LENGTH=5000
    #OPTIMIZER = Adamax(lr=0.002, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0) # Optimizer
    NB_CLASSES = 6 # number of outputs = number of classes
    INPUT_SHAPE = (LENGTH,1)

    #データセットロード
    x_train, y_train, x_valid, y_valid, x_test, y_test = loaddata()

    # Please refer to the dataset format in readme
    #K.set_image_dim_ordering("tf") # tf is tensorflow

    # Convert data as float32 type
    x_train = x_train.astype('float32')
    x_valid = x_valid.astype('float32')
    x_test = x_test.astype('float32')
    y_train = y_train.astype('float32')
    y_valid = y_valid.astype('float32')
    y_test = y_test.astype('float32')

    # we need a [Length x 1] x n shape as input to the DF CNN (Tensorflow)
    x_train = x_train[:, :,np.newaxis]
    x_valid = x_valid[:, :,np.newaxis]
    x_test = x_test[:, :,np.newaxis]

    print("学習サンプル")
    print(x_train.shape[0])
    print("検証サンプル")
    print(x_valid.shape[0])
    print("テストサンプル")
    print(x_test.shape[0])

    # Convert class vectors to categorical classes matrices
    y_train = keras.utils.to_categorical(y_train, NB_CLASSES)
    y_valid = keras.utils.to_categorical(y_valid, NB_CLASSES)
    y_test = keras.utils.to_categorical(y_test, NB_CLASSES)
    
    print("モデルをビルドして学習")
    model = DFNet.build(input_shape=INPUT_SHAPE, classes=NB_CLASSES)

    #model.compile(loss="categorical_crossentropy", optimizer=OPTIMIZER,
	#metrics=["accuracy"])

    model.compile(loss="categorical_crossentropy", optimizer=keras.optimizers.Adadelta(),
	metrics=["accuracy"])
    print("コンパイル完了")
    print("学習開始")
    # Start training
    history = model.fit(x_train, y_train,
		batch_size=BATCH_SIZE, epochs=NB_EPOCH,
		verbose=VERBOSE, validation_data=(x_valid, y_valid))
    
    # Start evaluating model with testing data
    score_test = model.evaluate(x_test, y_test, verbose=VERBOSE)
    print("Testing accuracy:", score_test[1])
def loaddata():

    print ("バイナリファイルからデータセット読み取り")
    # X represents a sequence of traffic directions
    # y represents a sequence of corresponding label (website's label)

    # Load training data
    with open("pickle/x_train.pickle", "rb") as handle:
        x_train = np.array(pickle.load(handle))
    with open("pickle/y_train.pickle", "rb") as handle:
        y_train = np.array(pickle.load(handle))

    # Load validation data
    with open("pickle/x_valid.pickle", "rb") as handle:
        x_valid = np.array(pickle.load(handle))
    with open("pickle/y_valid.pickle", "rb") as handle:
        y_valid = np.array(pickle.load(handle))

    # Load testing data
    with open("pickle/x_test.pickle", "rb") as handle:
        x_test = np.array(pickle.load(handle))
    with open("pickle/y_test.pickle", "rb") as handle:
        y_test = np.array(pickle.load(handle))
    print("各データセット:")
    print ("訓練データの特徴量:")
    print(x_train.shape)
    print ("訓練データのラベル:")
    print(y_train.shape)
    print ("検証データの特徴量:")
    print(x_valid.shape)
    print ("検証データのラベル:")
    print(y_valid.shape)
    print ("テストデータの特徴量:")
    print(x_test.shape)
    print ("テストデータのラベル:")
    print(y_test.shape)

    return x_train, y_train, x_valid, y_valid, x_test, y_test

main()