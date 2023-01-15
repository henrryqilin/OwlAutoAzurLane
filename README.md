
# Owl Auto Azur Lane
因为找到了ALAS开发周期已结束，未来会以另一个项目的形式继续开发

## 目录
- [安装说明](#01)
- [使用说明](#02)
- [开源库](#03)

<a name='01'></a>
## 安装说明

### 1、安装[python](https://www.python.org/)环境（自己找教程叭）
- 推荐3.7.8

### 2、安装[PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)
CPU用户
- 使用这行代码
```
	pip install paddlepaddle==2.3.2 -i https://pypi.tuna.tsinghua.edu.cn/simple
```
GPU用户（需要自行安装**CUDA**和**CUDNN**）
- 请根据自己的GPU情况使用[PaddleOCR的官方安装文档](https://www.paddlepaddle.org.cn/install/quick?docurl=/documentation/docs/zh/install/pip/windows-pip.html)

### 3、安装其他依赖
```
	pip install pyautogui
	pip install time
```

<a name='02'></a>
## 使用说明

### 1、打开*start.py*  

### 2、调整截图的范围
使用***develop.py***文件，参考***截图位置.txt***和***img***文件夹中***截图示例***文件夹中的示例图片进行调整   


### 3、打开碧蓝航线并切换到对应开始界面
以后会优化    
- **刷关**：章节列表，左上角有章节名字 ***(半成品，不建议使用）***   
- **演习**：主界面，有看板船（秘书舰）  
- **每日挑战**：主界面，有看板船

### 4、运行程序并立刻切到模拟器  
在***start.py***填上需要代理模式的代码
```
   oaa.find_and_start()	#刷关模式的函数
   oaa.exercises()	#演习模式的函数
   oaa.daily_challange()#每日挑战模式的函数
```
运行程序，挂机时需保证窗口最大化并且在**前台**

### ~~5、等待BUG出现~~   

<a name=03></a>
## 开源库
- 图像识别：[opencv](https://github.com/opencv/opencv.git)
- 文字识别：[PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)
- anywheretogo：[auto_player](https://github.com/anywheretogo/auto_player/blob/master/auto_player.py)
- 还有一个明日方舟自动刷1-7的代码，现在找不到了