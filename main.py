from cube import Cube 
from msvcrt import getch
import sys
from tool import window_capture
from getopt import getopt
from pywintypes import error as WindowCaptureError

serialUSB = 'COM5'
baudRate = 115200
mode, window = None

try:
	opts, arg = getopt(args=sys.argv[1:], shortopts='hs:b:', longopts=['mode=','window='])
except getopt.GetoptError:
	print('参数设置错误，使用:\n"python main.py -h"\n查看用法')
	sys.exit()

assert opts != [] , '请输入参数，使用:\n"python main.py -h"\n查看用法'

for opt, arg in opts:
	if opt == '-h':
		helper = '''使用方法：
python main.py --mode mode --window window [-s serialUSB -b baudRate]
其中，mode为运行模式，train为训练模式，run为使用模式
window为obs窗口句柄（十六进制）
serialUSB为Arduino端口，默认为com5
baudRate为Arduino波特率，默认为115200'''
		print(helper)
		sys.exit()
	if opt == '--mode':
		mode = arg
	if opt == '--window':
		window = arg
	if opt == '-s':
		serialUSB = arg
	if opt == '-b':
		baudRate = int(arg)

assert mode in ['run', 'train'] , 'mode参数有误，使用:\n"python main.py -h"\n查看用法'

try:
	window = int(window, 16)
	window_capture(window)
except WindowCaptureError, ValueError:
	print('obs窗口句柄有误，使用:\n"python main.py -h"\n查看用法')
	sys.exit()

if mode == 'train':
	print('放置完成后，按下回车开始训练！')
	while True:
		Input = getch()
		if Input == b'\r':
			break

	cube = Cube(train=True, window=window, serialUSB=serialUSB, baudRate=baudRate)

if mode == 'run':
	print('所有模块加载完成，按下回车开始！')
	while True:
		Input = getch()
		if Input == b'\r':
			break

	cube = Cube(train=False, window=window, serialUSB=serialUSB, baudRate=baudRate)
