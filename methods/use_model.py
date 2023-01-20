import joblib
from tensorflow.kears.models import load_model
from numpy import argmax


model_cnn = load_model('./models/cnn.h5')
model_stacking = joblib.load('./models/StackingClassifier.pkl')

def use_cnn(data, model):
	pre_result = model.predict(data)
	return argmax(pre_result)+1

def use_stacking(data, model):
	pre_result = model.predict(data)
	return pre_result[0]+1
	
