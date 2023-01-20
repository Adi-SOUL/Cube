# Cube

## 颜色对数字的映射
	红绿蓝白橙黄
	1 2 3 4 5 6
## 关于图像文件的存储与读取：
### 目录格式：
	|项目根目录\
	|——dataset\
	|————1\
	|——————001.jpg
	|———————......
	|————2\
	|——————001.jpg
	|......
	|————6\
	|——————001.jpg
	|——————......
	
### CNN所用的IO格式：
	X:28*28*3，Y:one-hot index
	程序接收的格式为：
	{[1,0,0,0,0]:[img1,img2,...],......} //img为array：详见getdata.py line:32

### stacking所用的IO格式：
	X:[R,G,B], Y:[num]
	程序接收的格式为：
	[(X, Y)...]
	
## 使用方法：

	pip install -r ./requirements.txt
	python main.py --mode mode --window window [-s serialUSB -b baudRate]

	其中，mode为运行模式，train为训练模式，run为使用模式
	window为obs窗口句柄（十六进制）
	serialUSB为Arduino端口，默认为com5
	baudRate为Arduino波特率，默认为115200
