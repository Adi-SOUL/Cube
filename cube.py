from cube_solve import CubeSolver
from methods.use_model import use_cnn, use_stacking, model_cnn, model_stacking
from tool import window_capture
from CNN import train_cnn
from stacking import train_stacking
import cv2 as cv
import threading
from time import time


class Cube:

	area = (10,10)
	coordinate = {
		'U': [[195, 45], [315, 45], [420, 45],
				[190, 95], [315, 95], [430, 95],
				[160, 165], [315, 165], [460, 165],],

		'F': [[160, 285], [315, 285], [460, 285],
				[190, 370], [315, 370], [430, 370],
				[195, 425], [305, 425], [415, 425],],

		'B': [[195, 45], [315, 45], [425, 45],
				[190, 100], [315, 100], [430, 100],
				[160, 180], [315, 180], [460, 180],],

		'D': [[160, 300], [315, 300], [460, 300],
				[190, 390], [315, 390], [435, 390],
				[195, 440], [315, 440], [425, 440],],

		'L': [[70, 80], [220, 80], [380, 80],
				[70, 230], [230, 230], [395, 230],
				[70, 370], [200, 410], [370, 370]],

		'R': [[70, 80], [210, 80], [360, 80],
				[30, 230], [210, 230], [360, 230],
				[70, 380], [210, 395], [360, 380]]
	}

	def __init__(self, train, window, serialPort="COM5", baudRate=115200):
		self.solver = cube_solve(serialPort=serialPort, baudRate=baudRate)
		if train:
			self.window = window
			train()
		else:
			self.img = window_capture(window)
			solve()

	def get_color(self, method, model):
		result = dict()

		def get_one_color(self, name, coordinate, area, method, model):
			full_img = self.img
			res = ''
			for point in coordinate[name]:
				img = full_img[point[0]-area[0]:point[0]+area[0]][point[1]-area[1]:point[1]+area[1]]
				color_index = method(img, model)
				res = res + str(color_index)
				result[name] = res

		thread_pool = [0]*6
		names = coordinate.keys()
		for i in range(6):
			thread_pool[i] = threading.Thread(target=get_one_color,args=(self,names[i],coordinate,area,method,model))
			thread_pool[i].start()
			continue
		thread_pool[0].join()
		thread_pool[1].join()
		thread_pool[2].join()
		thread_pool[3].join()
		thread_pool[4].join()
		thread_pool[5].join()

		return result

	def solve(self):
		color_ex = get_color(self, method=use_stacking, model=model_stacking)
		run = self.solver.run(color_ex)
		if not run:
			color_ex = get_color(self, method=use_cnn, model=model_cnn)
			self.solver.run(color_ex)


	def train(self):
		color_lists = {
			"U": "214325521",
			"R": "342543334",
			"F": "616456112",
			"D": "661266345",
			"L": "153631554",
			"B": "534214622",
		}
		print('收集图像中')
		for i in range(6):
			full_img = window_capture(self.window)
			names = coordinate.keys()
			for name in names:
				for point in coordinate[name]:
					img = full_img[point[0]-area[0]:point[0]+area[0]][point[1]-area[1]:point[1]+area[1]]

					path = './dataset//'+color_lists[name][i]+'//'+str(time())[:-8]+'.jpg'
					cv.imwrite(path, img)

			if i < 4:
				self.solver.SerialWrite('l')
			else:
				self.solver.SerialWrite('r')
			while True:
				return_msg = self.solver.dectString(self.solver.SerialUSB)
				if return_msg == 'end':
					break

		self.solver.close()

		print('图象收集完成\n开始训练神经网络')

		train_cnn()

		print('神经网络训练完成\n开始训练集成模型')

		train_stacking()

		print('训练完成')
