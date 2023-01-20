from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.models import Sequential

from getdata import data_for_cnn,data_split


def train_cnn():
    data,X_train,X_test,Y_train,Y_test = [list()]*5

    for key,value in data_for_cnn:
        for i in value:
            data.append((i, key))

    train, test = data_split(full_list=data, ratio=0.8)

    for train_X, train_Y in train:
        X_train.append(train_X)
        Y_train.append(train_Y)

    for test_X, test_Y in test:
        X_test.append(test_X)
        Y_test.append(test_Y)


    model = Sequential()
    model.add(Conv2D(32, kernel_size=(5, 5), strides=(1, 1),
                 activation='relu',
                 input_shape=(28,28,3)))
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
    model.add(Conv2D(64, (5, 5), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dense(1000, activation='relu'))
    model.add(Dense(6, activation='softmax'))

    model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adam(),
              metrics=['accuracy'])


    model.fit(X_train, Y_train,
          batch_size=128,
          epochs=100,
          verbose=1,
          validation_data=(X_test, Y_test))

    model.save('./models/cnn.h5')

    score = model.evaluate(X_test, Y_test, verbose=0)
    print('Test loss:', score[0])
    print('Test accuracy:', score[1])
