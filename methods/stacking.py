from getdata import data_for_stacking,data_split

from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier,StackingClassifier

import joblib


def train_stacking():
	train, test = data_split(full_list=data_for_stacking, ratio=0.8)

	X_train,X_test,Y_train,Y_test = [list()]*4

    for train_X, train_Y in train:
	X_train.append(train_X)
        Y_train.append(train_Y)

    for test_X, test_Y in test:
        X_test.append(test_X)
        Y_test.append(test_Y)

	lr = LogisticRegression(dual=False,random_sate=0,n_jobs=-1)
	svc = SVC(kernel='rbf',random_sate=0,gamma=0.20)
	dectree = DecisionTreeClassifier(criterion='gini',max_depth=4,random_sate=0)
	knc = KNeighborsClassifier(n_jobs=-1)
	gpc = GaussianProcessClassifier(n_jobs=-1)
	abc = AdaBoostClassifier(learning_rate=.5,random_sate=0)

	estimators = [
		('lr', lr),
		('svc',svc),
		('dectree',dectree),
		('knc',knc),
		('gpc',gpc),
		('abc',abc)]

	sc = StackingClassifier(estimators=estimators,final_estimator=RandomForestClassifier(),n_jobs=-1)
	sc.fit(X_train, Y_train)

	joblib.dump(sc,'./models/StackingClassifier.pkl')
