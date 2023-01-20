import numpy as np
import win32gui, win32ui, win32con, win32api
from pywintypes import error as WindowCaptureError
import cv2 as cv

def window_capture(hwnd):
	hwndDC = win32gui.GetWindowDC(hwnd)
	mfcDC = win32ui.CreateDCFromHandle(hwndDC)
	saveDC = mfcDC.CreateCompatibleDC()
	saveBitMap = win32ui.CreateBitmap()
	left, top, right, bot = win32gui.GetWindowRect(hwnd)
	w = right - left
	h = bot - top
	saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
	saveDC.SelectObject(saveBitMap)
	saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, 0), win32con.SRCCOPY)
	signedIntsArray = saveBitMap.GetBitmapBits(True)
	img = np.fromstring(signedIntsArray, dtype='uint8')
	img.shape = (h,w,4) 
	return img[::,::,:3:]


if __name__ == '__main__':
	import time
	time_1 = time.time()
	try:
		img = window_capture(2886388)
		print(time.time()-time_1)
		cv.imshow('test',img)
		cv.waitKey(0)
	except WindowCaptureError:
		pass