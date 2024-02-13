# Copyright Airbus Helicopters 2024

import pickle
import os
from tensorflow import keras
from JSON_from_keras_model import JSON_from_keras_model
from skl2onnx import to_onnx
import numpy as np

'''
convert sklearn pickle MLP to keras model
'''
def pickle2keras(fname):
    # instanciate the destination keras model
    model = keras.models.Sequential()
    with open(os.path.abspath(fname),"rb") as f:
        # get LDR input model params 
        mlp = pickle.load(f)['Models']['MLP']
        # get MLP model weights  
        c = mlp.coefs_
        # get MLP model bias  
        b = mlp.intercepts_
        # for each input model layer 
        for i in range(len(c)):
            shape = np.array(c[i]).shape
            layer = keras.Input(shape=(shape[0],) ) if i==0 else keras.layers.Dense(shape[0], activation='relu')
            model.add(layer)
        # regression layer
        model.add(keras.layers.Dense(1, activation='relu'))
        # build destination keras model 
        model.build((None, 1))

        # setting weights from sklearn to keras 
        for i in range(len(c)):
            layer = model.get_layer(index=i)
            layer.set_weights((c[i],b[i]))
    return model

''' 
convert sklearn pickle MLP to acetone json model
'''
def pickle2json(filelist, destination):
    #iterate on model files 
    for fname in filelist:
        outname = os.path.abspath(destination+os.path.basename(fname).replace('.txt','.json'))
        print('pickle to keras : '+outname)
        JSON_from_keras_model(pickle2keras(fname), outname)

''' 
convert sklearn pickle MLP to onnx model
'''
def pickle2onnx(filelist,destination):
    #iterate on model files 
    for fname in filelist:
        with open(fname,"rb") as f:
            m = pickle.load(f)
            X=np.array([1.0])
            X = X.astype(np.float32)
            onx = to_onnx(m["Models"]["MLP"],X[:1])
            outname = os.path.abspath(destination+os.path.basename(fname).replace('.txt','.onnx'))
            print('pickle to onnx : '+outname)
            with open(outname,"wb") as out:
                out.write(onx.SerializeToString())

