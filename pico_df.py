import pickle
import numpy as np
import keras
from keras import backend as K
from utility import LoadDataNoDefCW
from Model_NoDef import DFNet
import random
from keras.utils import np_utils
from keras.optimizers import Adamax
import os

def main():
    #データセットロード
    x_train, y_train, x_valid, y_valid, x_test, y_test = loaddata()

def loaddata():

    print ("バイナリファイルからデータセット読み取り")
    # X represents a sequence of traffic directions
    # y represents a sequence of corresponding label (website's label)

    # Load training data
    with open("pickle/x_train.pkl", "rb") as handle:
        x_train = np.array(pickle.load(handle))
    with open("pickle/y_train.pkl", "rb") as handle:
        y_train = np.array(pickle.load(handle))

    # Load validation data
    with open("pickle/x_valid.pkl", "rb") as handle:
        x_valid = np.array(pickle.load(handle))
    with open("pickle/y_valid.pkl", "rb") as handle:
        y_valid = np.array(pickle.load(handle))

    # Load testing data
    with open("pickle/x_test.pkl", "rb") as handle:
        x_test = np.array(pickle.load(handle))
    with open("pickle/y_test.pkl", "rb") as handle:
        y_test = np.array(pickle.load(handle))
    print("各データセット:")
    print ("訓練データの特徴量:" + x_train.shape)
    print ("訓練データのラベル:" + y_train.shape)
    print ("検証データの特徴量:" + x_valid.shape)
    print ("検証データのラベル:" + y_valid.shape)
    print ("テストデータの特徴量:" + x_test.shape)
    print ("テストデータのラベル:" + y_test.shape)

    return x_train, y_train, x_valid, y_valid, x_test, y_test

main()