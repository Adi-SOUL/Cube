import os
from keras.preprocessing import image
from numpy import argmax


def data_split(full_list, ratio, shuffle=True):
    n_total = len(full_list)
    offset = int(n_total * ratio)
    if n_total == 0 or offset < 1:
        return [], full_list
    if shuffle:
        random.shuffle(full_list)
    list_train = full_list[:offset]
    list_test = full_list[offset:]
    return list_train, list_test


def get_data_for_cnn():
    res = dict()
    pre_Y = [0]*6
    for color_set in os.listdir('./dataset'):
        i = 0
        try:
            pic_names = os.listdir('./dataset//'+color_set)
            Y = pre_Y
            Y[i] = 1
            X = list()
            for pic in pic_names:
                path = './dataset//'+color_set+'//'+pic
                img = image.load_img(path,target_size=(28,28))
                img = image.img_to_array(img) / 255.0
                X.append(img)
            res[Y]=X
        except NotADirectoryError:
            pass
    return res 


data_for_cnn = get_data_for_cnn()

def get_data_for_stacking(raw_data=data_for_cnn):
    res = list()
    for key in raw_data:
        label = [argmax(key)]
        for pic in raw_data[key]:
            R,G,B = (0,0,0)
            for i in range(28)：
                for j in range(28):
                    R = R + pic[i][j][0]
                    G = G + pic[i][j][1]
                    B = B + pic[i][j][2]
            R_mean = R/(28*28)
            G_mean = G/(28*28)
            B_mean = B/(28*28)

        res_pic = ([R_mean,G_mean,B_mean],label)
        res.append(res_pic)

    return res 

data_for_stacking = get_data_for_stacking(data_for_cnn)

