if __name__ == '__main__' :
	print('这是basic程序，不是启动程序')

import cv2,pyautogui,time
from paddleocr import PaddleOCR
from setting import *

ocr = PaddleOCR(use_angle_cls=False, lang="ch")

def log_write(str = '',aim = './logs/dlog.txt',mode = 'a') :
	"""
		将指定的字符按指定的模式写入指定文件
		aim:str类型，文件名或'./logs/log.txt'
		mode:str类型，'w'以写入的方式打开文件，会覆盖已存在的文件'a'以写入模式打开，如果文件存在，则在末尾追加写入
		str:str类型，写入的内容
		return:none
	"""
	log = open(aim,mode)
	log.write(str)
	log.close()
	return#log_write

def get_screen(shot_change = None,save_location = './imgs/screenshot.png')	:
	"""
		截取屏幕
		shot_change:tuple类型，偏移的坐标，(x坐标，y坐标，x轴长度，y轴长度)
		save_location:str类型，截图保存的地址
		return:None
	"""
	pyautogui.screenshot(region = shot_change).save(save_location)
	return#get_screen

def click_change(clickpoint,changex = 0,changey = 0,sleep = 1)	:
	"""
		输入一个元组，左键点击给定的位置，可偏移
		clickpoint:tuple类型，点击的xy坐标
		x,y:int类型，xy坐标的偏移量
		return:None
	"""
	clickx = clickpoint[0]
	clicky = clickpoint[1]
	pyautogui.click(clickx + changex,clicky + changey,button='left')
	time.sleep(sleep)
	return#click_change

def ocr_result(location = './imgs/screenshot.png') :
	"""
		显示图片中所有识别到的结果
		location：str类型，图片地址(相对地址和绝对地址均可)
		return:list类型，包含paddleOCR返回的所有结果
	"""
	result = ocr.ocr(location, cls=True)
	return result#ocr_result

def ocr_extract(location = './imgs/screenshot.png') :
	"""
		将OCR识别的结果提取出来
		result:list类型，ocr_result识别的结果
		return:list类型，
	"""
	result = ocr.ocr(location, cls=True)
	all_menmber = []
	
	for line in result:
		all_menmber.append(line[1][0])

	return all_menmber#ocr_extract

def find_object(aim,location = './imgs/screenshot.png') :
	"""
		基于paddleOCR，找到目标的坐标
		aim:str类型，目标的名称
		location：str类型，图片地址，相对地址和绝对地址均可
		return:tuple类型,为目标的xy坐标
	"""
	
	ocr = PaddleOCR(use_angle_cls=True, lang="ch")  #不能使用多线程
	result = ocr.ocr(location, cls=True)
	
	for line in result:
		find_check = 0
		
		if line[1][0] == aim :
			find_check = 1
			left_up = line[0][0]
			right_down = line[0][2]
			aim_location = ((left_up[0] + right_down[0]) / 2,(left_up[1] + right_down[1]) / 2)

	if find_check == 0 :
		print('寄，找不到了捏')
		assert 9 > 10

	return aim_location#find_object
