import pickle
import numpy as np
import keras
from keras import backend as K
from pico_df_model import Pico_model
from keras.optimizers import Adamax

def loaddata():

    print ("バイナリファイルからデータセット読み取り")
    #学習データロード
    with open("pickle/x_train.pkl", "rb") as handle:
        x_train = np.array(pickle.load(handle))
    with open("pickle/y_train.pkl", "rb") as handle:
        y_train = np.array(pickle.load(handle))

    #検証データロード
    with open("pickle/x_valid.pkl", "rb") as handle:
        x_valid = np.array(pickle.load(handle))
    with open("pickle/y_valid.pkl", "rb") as handle:
        y_valid = np.array(pickle.load(handle))

    #テストデータロード
    with open("pickle/x_test.pkl", "rb") as handle:
        x_test = np.array(pickle.load(handle))
    with open("pickle/y_test.pkl", "rb") as handle:
        y_test = np.array(pickle.load(handle))

    print("各データセット数:")
    print ("学習データの特徴量/ラベル:" + str(x_train.shape) + "/" + str(y_train.shape))
    print ("検証データの特徴量/ラベル:" + str(x_valid.shape) + "/" + str(y_valid.shape))
    print ("テストデータの特徴量/ラベル:" + str(x_test.shape) + "/" + str(y_test.shape))

    return x_train, y_train, x_valid, y_valid, x_test, y_test

def main():
    print("DFモデルの学習と評価開始")
    #エポック数
    EPOCH=30
    #バッチサイズ
    BATCH_SIZE=128
    #ログ指定(1エポックごとにログ出力)
    VERBOSE=2
    #パケットシーケンス長さ指定
    LENGTH=5000
    #OPTIMIZER = Adamax(lr=0.002, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0) # Optimizer
    #クラスの数指定
    NB_CLASSES=5
    #入力の型指定
    INPUT_SHAPE = (LENGTH,1)

    #データセットロード
    x_train, y_train, x_valid, y_valid, x_test, y_test = loaddata()

    #バックエンドをtensorflowに指定
    #K.set_image_dim_ordering("tf") # tf is tensorflow

    #データをfloat32に変換
    x_train = x_train.astype('float32')
    x_valid = x_valid.astype('float32')
    x_test = x_test.astype('float32')
    y_train = y_train.astype('float32')
    y_valid = y_valid.astype('float32')
    y_test = y_test.astype('float32')

    #学習の入力に[length*1]*nを必要とするのでnp.newaxisで新たな次元を追加する
    x_train = x_train[:, :,np.newaxis]
    x_valid = x_valid[:, :,np.newaxis]
    x_test = x_test[:, :,np.newaxis]

    print("学習サンプル:" + str(x_train.shape[0]))
    print("検証サンプル:" + str(x_valid.shape[0]))
    print("テストサンプル:" + str(x_test.shape[0]))

    #ラベルをベクトルに変換する
    y_train = keras.utils.to_categorical(y_train, NB_CLASSES)
    y_valid = keras.utils.to_categorical(y_valid, NB_CLASSES)
    y_test = keras.utils.to_categorical(y_test, NB_CLASSES)
    
    print("モデルをビルドして学習")
    model = Pico_model.build(input_shape=INPUT_SHAPE, classes=NB_CLASSES)
    model.compile(loss="categorical_crossentropy", optimizer=keras.optimizers.Adadelta(),
	metrics=["accuracy"])

    print("コンパイル完了")
    print("学習開始")
    history = model.fit(x_train, y_train,
		batch_size=BATCH_SIZE, epochs=EPOCH,
		verbose=VERBOSE, validation_data=(x_valid, y_valid))
    
    # Start evaluating model with testing data
    score_test = model.evaluate(x_test, y_test, verbose=VERBOSE)
    print("テスト精度:", score_test[1])

main()