if __name__ == '__main__' :
	print('这是主程序，不是启动程序')

import cv2,pyautogui,time,numpy
from paddleocr import PaddleOCR, draw_ocr
from setting import *

#————————————————————————————————————————————————————————————

location_screenshot = './imgs/screenshot.png'
exercises_loaction = [(335,400,130,75),(670,400,130,75),(1005,400,130,75),(1340,400,130,75)]

def get_screen(shot_change = None,save_location = './imgs/screenshot.png')	:
	"""
		截取屏幕
		shot_change:tuple类型，偏移的坐标，(x坐标，y坐标，x轴长度，y轴长度)
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

def show_result(location = './imgs/screenshot.png') :
	"""
		显示图片中所有识别到的结果
		location：str类型，图片地址(相对地址和绝对地址均可)
		return:list类型，包含paddleOCR返回的所有结果
	"""
	ocr = PaddleOCR(use_angle_cls=True, lang="ch")  #不能使用多线程
	result = ocr.ocr(location, cls=True)
	return result

def find_object(aim,location = './imgs/screenshot.png') :
	"""
		基于paddleOCR，找到目标的坐标
		aim:str类型，目标的名称
		location：str类型，图片地址，相对地址和绝对地址均可
		return:tuple类型,为目标的xy坐标
	"""
	
	ocr = PaddleOCR(use_angle_cls=True, lang="ch")  #不能使用多线程
	result = ocr.ocr(location, cls=True)
	objective = ()
	
	for line in result:
		find_check = 0
		#print(line)
		recognize_result = line[1][0]
		
		if recognize_result == aim :
			find_check = 1
			left_up = line[0][0]
			right_down = line[0][2]
			aim_location = ((left_up[0] + right_down[0]) / 2,(left_up[1] + right_down[1]) / 2)

	if find_check == 0 :
		print('寄，找不到了捏')
		assert 9 > 10

	return aim_location

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
		print(result_matrix[1],)
		print('寄，找不到了捏')
		assert 9 > 10
		return 

	upper_left = result_matrix[3]	
	lower_right = (upper_left[0] + width, upper_left[1] + height)
	avg = (int((upper_left[0] + lower_right[0]) / 2), int((upper_left[1] + lower_right[1]) / 2))	
	# 计算坐标的平均值并将其返回
	return avg

#——————————————————————————————————————定义调用分割线——————————————————————————————————————————————————

def chapter_orientation(chapter_name)	:
	"""
		定位章节
		chapter_name:str类型。章节的名字
		return:None
	"""
	get_screen(shot_change = (344,129,365,58))
	all_result = show_all_menmber()
	# print(all_result)
	check = 0
	for line in all_result	:
		if chapter_name == line :
			check = 1
			time.sleep(1)
			return
	
	for roll in range(10) :	#返回第一章
		click_change((1739,555))
		time.sleep(0.3)
		# get_screen()
		# all_result = show_all_menmber()
		# # print(all_result)
		# for line in all_result	:
		# 	if '目标地图尚未开放' in line  :
		# 		time.sleep(3)
		# 		return

	for roll in range(15)	:
		get_screen(shot_change = (344,129,365,58))
		all_result = show_all_menmber()
		for line in all_result :
			if chapter_name == line :
				check = 1
				time.sleep(0.5)
				return
			else	:
				click_change((128,555))
	
	if check == 0 :
		print('寄，找不到了捏')
		assert 9 > 10
	return

def level_orientation(level_name)	:
	'''
		定位关卡
		level_name:str类型，以数字形式提供如:1-1,C3等
		return:tuple类型，关卡的坐标
	'''
	time.sleep(3)
	get_screen()
	all_result = show_result()
	# print(all_result)
	for line in all_result :
		exchange0 =	line [1] 
		recognize_result = exchange0[0]
		if level_name in recognize_result :
			exchange1 = line[0]
			return_location = exchange1[1]
			return return_location
	return (0,0)

def immediate_start() :
	'''
		点击立刻前往并继续刷体力
		return:None
	'''
	time.sleep(1)
	get_screen()
	click_change(get_xy('./imgs/models/immediate_start.png'))
	time.sleep(1)
	get_screen()
	click_change(get_xy('./imgs/models/immediate_start.png'))
	return

def fighting_check() :
	time.sleep(60)
	battling = 1
	
	while battling > 0 :
		get_screen()
		all_result = show_all_menmber()
		print(all_result)
		if '再次前往' in all_result :
			battling = 0
			all_result = show_result()
			for line in all_result :
				exchange0 =	line [1] 
				recognize_result = exchange0[0]
				if '再次前往' in recognize_result :
					exchange1 = line[0]
					return_location = exchange1[1]
		else :
			time.sleep(5)

	time.sleep(1)
	return return_location

#——————————————————————————————main——————————————————————————————

def find_and_start() :
	chapter_orientation('所罗门的噩梦上')
	click_change(level_orientation('4-4'))
	immediate_start()
	again = fighting_check()
	
	while repetition > 0 :
		time.sleep(1)
		click_change(again)
		# time.sleep(100000) #没写完呢,下面是检测理智是否充足的代码
		# get_screen()
		again = fighting_check()
		repetition -= 1
	
	return

def exercises() :
	'''
		从主界面开始独立完成演习
		return:None
	'''
	time.sleep(1)
	get_screen()
	click_change(get_xy('./imgs/models/weigh_anchor.png'))
	time.sleep(1.5)
	get_screen()
	click_change(get_xy('./imgs/models/exercises.png'))
	time.sleep(1.5)
	get_screen((1630,234,84,30))
	all_result = show_all_menmber()
	locationg = all_result[0].find('/')
	n = int(all_result[0][0:locationg])
	refresh_time = 3
	
	while n > 0 :
		exercises_aim = 4000000
		n -= 1
		
		for i in exercises_loaction :
			get_screen(shot_change = i)
			exercises_list = show_all_menmber()
			exercises_strength = int(exercises_list[0]) + int(exercises_list[1])
			if exercises_strength < exercises_aim :
				exercises_aim = exercises_strength
				exercises_list = show_result()
				click_location = tuple(exercises_list[0][0][0])
				click_changex = int(i[0])
				click_changey = int(i[1])

		if refresh_time > 0 and exercises_aim > 1.2 * (pioneer_power + major_power) :
			click_change(get_xy('./imgs/models/new_opponent.png'))
			refresh_time -= 1
			n += 1
			time.sleep(5)
			break
		click_change(click_location,click_changex,click_changey)
		time.sleep(1)
		get_screen()
		click_change(get_xy('./imgs/models/exercises_start.png'))
		time.sleep(1)
		get_screen()
		click_change(get_xy('./imgs/models/attack.png'))
		time.sleep(10)
		battling = 1
		
		while battling > 0 :
			get_screen()
			all_result = show_all_menmber()
			# print(all_result)
			if '战斗评价' in all_result or '点击继续' in all_result :
				battling = 0
				all_result = show_result()
				for line in all_result :
					exchange0 =	line [1] 
					recognize_result = exchange0[0]
					if '战斗评价' in recognize_result or '点击继续' in recognize_result :
						return_location = line[0][1]
			else :
				time.sleep(5)

		click_change(return_location)
		time.sleep(2)
		click_change((937, 973))
		time.sleep(2)
		click_change((928,882))
		time.sleep(8)
		click_change(get_xy('./imgs/models/confirm.png'))
		time.sleep(5)

	get_screen()
	click_change(get_xy('./imgs/models/home.png'))

def daily_challenge() :
	'''
		从主界面开始完成每日挑战
		return：None
	'''
	time.sleep(1)
	get_screen()
	click_change(get_xy('./imgs/models/weigh_anchor.png'))
	time.sleep(2)
	get_screen()
	click_change(get_xy('./imgs/models/daily_challange.png'))
	time.sleep(2)
	get_screen((780,195,65,35))
	all_result = show_all_menmber()

	if all_result[0][0] == 0 :
		daily_check = 0		#0打完了，1没有打
	else :
		daily_check = 1
	get_screen((1160,250,55,35))

	all_result = show_all_menmber()

	if all_result[0][0] == 0 :
		weekly_check = 0
	else :
		weekly_check = 1
	
	if daily_check == 0 and weekly_check == 0 :
		pass
	elif daily_check == 1 and weekly_check == 0 :
		click_change((865,570))
		time.sleep(2)
		click_change((625,338))
		time.sleep(2)
		get_screen()
		click_change(get_xy('./imgs/models/sweep.png'))
		time.sleep(1)
		click_change((830,880))
		time.sleep(1)
		get_screen()
		click_change(get_xy('./imgs/models/return.png'))
		time.sleep(1)

		for i in range(3) :
			click_change((1760,530))#切换挑战项目
			time.sleep(2)
			get_screen((780,530,185,40))#识别是否开放
			all_result = show_all_menmber()

			if '今日未开放' in all_result :
				continue

			click_change((865,570))#进入挑战项目
			time.sleep(2)
			get_screen((630,343,385,40))#判断是不是商船护送
			all_result = show_all_menmber()

			if '商船护送(火力)' in all_result :#是商船护送
				if escort == 0 :
					pass
				else :
					click_change(find_object('商船护送(空域)'))
					time.sleep(1)
					click_change(get_xy('./imgs/models/sweep.png'))
					time.sleep(1)
					click_change((830,880))#点击关闭
					time.sleep(1)
					get_screen()
					click_change(get_xy('./imgs/models/return.png'))
					time.sleep(1)
					continue#跳出循环

			click_change((625,338))#
			time.sleep(1)
			get_screen()
			click_change(get_xy('./imgs/models/sweep.png'))
			time.sleep(1)
			click_change((830,880))#点击关闭
			time.sleep(1)
			get_screen()
			click_change(get_xy('./imgs/models/return.png'))
			time.sleep(1)

	elif daily_check == 1 and weekly_check == 1 :
		click_change((865,570))
		time.sleep(2)
		click_change((625,338))
		time.sleep(2)
		get_screen()
		click_change(get_xy('./imgs/models/sweep.png'))
		time.sleep(1)
		click_change((830,880))
		time.sleep(1)
		get_screen()
		click_change(get_xy('./imgs/models/return.png'))
		time.sleep(1)
		for i in range(6) :
			click_change((1760,530))#切换挑战项目
			time.sleep(2)
			get_screen((780,530,185,40))#识别是否开放
			all_result = show_all_menmber()

			if '今日未开放' in all_result :
				continue

			click_change((865,570))#进入挑战项目
			time.sleep(2)
			get_screen((630,343,385,40))#判断是不是商船护送
			all_result = show_all_menmber()

			if '商船护送(火力)' in all_result :#是商船护送
				if escort == 0 :
					pass
				else :
					click_change(find_object('商船护送(空域)'))
					time.sleep(1)
					click_change(get_xy('./imgs/models/sweep.png'))
					time.sleep(1)
					click_change((830,880))#点击关闭
					time.sleep(1)
					get_screen()
					click_change(get_xy('./imgs/models/return.png'))
					time.sleep(1)
					continue#跳出循环

			click_change((625,338))#
			time.sleep(1)
			get_screen()
			click_change(get_xy('./imgs/models/sweep.png'))
			time.sleep(1)
			click_change((830,880))#点击关闭
			time.sleep(1)
			get_screen()
			click_change(get_xy('./imgs/models/return.png'))
			time.sleep(1)
	
	time.sleep(2)
	get_screen()
	click_change(get_xy('./imgs/models/home.png'))
	time.sleep(2)
	return
