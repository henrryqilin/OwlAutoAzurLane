from paddleocr import PaddleOCR, draw_ocr
import cv2,pyautogui,time,numpy
from setting import *

def get_screen(shot_change = None,save_location = './imgs/screenshot.png')	:
	"""
		截取屏幕
		shot_change:tuple类型，偏移的坐标，(x坐标，y坐标，横向长度，纵向宽度)
		save_location:str类型，截图保存的地址
		return:None
	"""
	pyautogui.screenshot(region = shot_change).save(save_location)
	return

def click_change(clickpoint,changex = 0,changey = 0)	:
	"""
		输入一个元组，左键点击给定的位置，可偏移
		clickpoint:tuple类型，点击的xy坐标
		x,y:int类型，xy坐标的偏移量
		return:None
	"""
	clickx = clickpoint[0]
	clicky = clickpoint[1]
	pyautogui.click(clickx + changex,clicky + changey,button='left')
	return

def show_all_menmber(location = './imgs/screenshot.png') :
	"""
		显示图片中所有识别到的元素
		location：str类型，图片地址(相对地址和绝对地址均可)
		return:list类型，仅包含所有识别到的元素
	"""
	ocr = PaddleOCR(use_angle_cls=True, lang="ch")  #不能使用多线程
	result = ocr.ocr(location, cls=True)
	all_menmber = []
	for line in result:
		# print(line)	#调试用，查看所有识别结果和位置
		menmber_tuple = line[1]
		recognize_result = menmber_tuple[0]
		all_menmber.append(recognize_result)
	return all_menmber

def move_to(location) :
	pyautogui.moveTo(location[0],location[1],duration = 0.3)
	return

def get_mouse_location():
	"""
		获取鼠标坐标
		return:tuple类型，包含鼠标的坐标
	"""
	time.sleep(1)
	mouse_location = str(pyautogui.position())
	locationd = mouse_location.find(',')
	locationk = mouse_location.find(')')
	mousex = mousey = 0
	mousex = int(mouse_location[8:locationd])
	mousey = int(mouse_location[locationd + 4:locationk])
	# print(mouse_location)
	return (mousex,mousey)

def show_result(location = './imgs/screenshot.png') :
	"""
		显示图片中所有识别到的结果
		location：str类型，图片地址(相对地址和绝对地址均可)
		return:list类型，包含paddleOCR返回的所有结果
	"""
	ocr = PaddleOCR(use_angle_cls=True, lang="ch")  #不能使用多线程
	result = ocr.ocr(location, cls=True)
	return result

def get_xy(img_model_path):
	"""
	    用来判定游戏画面的点击坐标
	    img_model_path:用来检测的图片
	    return:tuple类型，返回检测到的区域中心的坐标
	"""
	img = cv2.imread("./imgs/screenshot.png")	# 待读取图像
	img_terminal = cv2.imread(img_model_path)	# 图像模板
	height, width, channel = img_terminal.shape	# 读取模板的高度宽度和通道数
	result = cv2.matchTemplate(img, img_terminal, cv2.TM_CCOEFF_NORMED)	# 使用matchTemplate进行模板匹配（标准平方差匹配）
	#TM_SQDIFF,--TM_SQDIFF_NORMED--
	result_matrix = cv2.minMaxLoc(result)# 解析出匹配区域的左上角图标,最小值在前最大值在后
	print(result_matrix[1])
	if result_matrix[1] < treshold :
		i = 3
		
		while result_matrix[1] < treshold and i > 0 :
			time.sleep(1)
			get_screen()
			img = cv2.imread("./imgs/screenshot.png")	# 待读取图像
			img_terminal = cv2.imread(img_model_path)	# 图像模板
			height, width, channel = img_terminal.shape	# 读取模板的高度宽度和通道数
			result = cv2.matchTemplate(img, img_terminal, cv2.TM_CCOEFF_NORMED)	# 使用matchTemplate进行模板匹配（标准平方差匹配）
			result_matrix = cv2.minMaxLoc(result)# 解析出匹配区域的左上角图标,最小值在前最大值在后
			print(result_matrix[1])
			i -= 1
	
	if result_matrix[1] < treshold :
		print(result_matrix[1])
		print('寄，找不到了捏')
		assert 9 > 10
		return 

	upper_left = result_matrix[3]	
	lower_right = (upper_left[0] + width, upper_left[1] + height)
	avg = (int((upper_left[0] + lower_right[0]) / 2), int((upper_left[1] + lower_right[1]) / 2))	
	# 计算坐标的平均值并将其返回
	return avg

#————————————————————————————————————————————————————————————————————————

#get_xy('./imgs/models/daily_challange.png')
get_screen()