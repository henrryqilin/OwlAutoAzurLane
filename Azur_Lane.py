#coding=utf-8

if __name__ == '__main__' :
	print('这是主程序，不是启动程序')

import time
from dbasic import get_screen,click_change,ocr_result,ocr_extract,find_object,get_xy,log_write
from paddleocr import PaddleOCR
from setting import *

#————————————————————————————————————————————————————————————
log_write(mode = 'w',str = '开始运行')
ocr = PaddleOCR(use_angle_cls=True, lang="ch")
log_write('OCR启动成功')
exercises_loaction = [(335,400,130,75),(670,400,130,75),(1005,400,130,75),(1340,400,130,75)]

#——————————————————————————————————————定义调用分割线——————————————————————————————————————————————————

def chapter_orientation(chapter_name)	:
	"""
		定位章节
		chapter_name:str类型。章节的名字
		return:None
	"""
	get_screen(shot_change = (344,129,365,58))
	all_result = ocr_extract()
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

	for roll in range(15)	:
		get_screen(shot_change = (344,129,365,58))
		all_result = ocr_extract()
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
	all_result = ocr_result()
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
		all_result = ocr_extract()
		print(all_result)
		if '再次前往' in all_result :
			battling = 0
			all_result = ocr_result()
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
	
	return#find_and_start

def exercises() :
	'''
		从主界面开始独立完成演习
		return:None
	'''
	time.sleep(1)
	get_screen()
	click_change(get_xy('./imgs/models/weigh_anchor.png'))
	#time.sleep(0.5)
	get_screen()
	click_change(get_xy('./imgs/models/exercises.png'))
	#time.sleep(1.5)
	get_screen((1630,234,84,30))
	all_result = ocr_extract()
	locationg = all_result[0].find('/')
	n = int(all_result[0][0:locationg])
	refresh_time = 3
	
	while n > 0 :
		exercises_aim = 4000000
		n -= 1
		
		for i in exercises_loaction :
			get_screen(shot_change = i)
			exercises_list = ocr_extract()
			exercises_strength = int(exercises_list[0]) + int(exercises_list[1])
			if exercises_strength < exercises_aim :
				exercises_aim = exercises_strength
				exercises_list = ocr_result()
				click_location = tuple(exercises_list[0][0][0])
				click_changex = int(i[0])
				click_changey = int(i[1])

		if refresh_time > 0 and exercises_aim > 1.2 * (pioneer_power + major_power) :
			get_screen()
			click_change(get_xy('./imgs/models/new_opponent.png'))
			refresh_time -= 1
			n += 1
			time.sleep(5)
			break

		click_change(click_location,click_changex,click_changey)
		get_screen()
		click_change(get_xy('./imgs/models/exercises_start.png'))
		get_screen()
		click_change(get_xy('./imgs/models/attack.png'))
		time.sleep(10)
		battling = 1
		
		while battling > 0 :
			get_screen()
			all_result = ocr_extract()
			# print(all_result)
			if '战斗评价' in all_result or '点击继续' in all_result :
				battling = 0
				all_result = ocr_result()
				for line in all_result :
					exchange0 =	line [1] 
					recognize_result = exchange0[0]
					if '战斗评价' in recognize_result or '点击继续' in recognize_result :
						return_location = line[0][1]
			else :
				time.sleep(5)

			for i in range(5) :
				click_change(sleep = 0.2,)
		click_change(get_xy('./imgs/models/confirm.png'))
		time.sleep(5)

	get_screen()
	click_change(get_xy('./imgs/models/home.png'))#exercises

def daily_challenge() :
	'''
		从主界面开始完成每日挑战
		return：None
	'''
	time.sleep(1)
	get_screen()
	click_change(get_xy('./imgs/models/weigh_anchor.png'))
	#time.sleep(1)
	get_screen()
	click_change(get_xy('./imgs/models/daily_challange.png'))
	#time.sleep(1)
	get_screen((780,195,65,35))
	all_result = ocr_extract()

	if all_result[0][0] == 0 :
		daily_check = 0		#0打完了，1没有打
	else :
		daily_check = 1
	get_screen((1160,250,55,35))

	all_result = ocr_extract()

	if all_result[0][0] == 0 :
		weekly_check = 0
	else :
		weekly_check = 1
	
	if daily_check == 0 and weekly_check == 0 :
		pass
	elif daily_check == 1 and weekly_check == 0 :
		click_change((865,570))
		#time.sleep(2)
		click_change((625,338))
		#time.sleep(2)
		get_screen()
		click_change(get_xy('./imgs/models/sweep.png'))
		click_change((830,880))
		get_screen()
		click_change(get_xy('./imgs/models/return.png'))

		for i in range(3) :
			click_change((1760,530))#切换挑战项目
			#time.sleep(2)
			get_screen((780,530,185,40))#识别是否开放
			all_result = ocr_extract()

			if '今日未开放' in all_result :
				continue

			click_change((865,570))#进入挑战项目
			get_screen((630,343,385,40))#判断是不是商船护送
			all_result = ocr_extract()

			if '商船护送(火力)' in all_result :#是商船护送
				if escort == 0 :
					pass
				else :
					click_change(find_object('商船护送(空域)'))
					click_change(get_xy('./imgs/models/sweep.png'))
					click_change((830,880))#点击关闭
					get_screen()
					click_change(get_xy('./imgs/models/return.png'))
					continue#跳出循环

			click_change((625,338))#
			get_screen()
			click_change(get_xy('./imgs/models/sweep.png'))
			click_change((830,880))#点击关闭
			get_screen()
			click_change(get_xy('./imgs/models/return.png'))

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
			all_result = ocr_extract()

			if '今日未开放' in all_result :
				continue

			click_change((865,570))#进入挑战项目
			time.sleep(2)
			get_screen((630,343,385,40))#判断是不是商船护送
			all_result = ocr_extract()

			if '商船护送(火力)' in all_result :#是商船护送
				if escort == 0 :
					pass
				else :
					get_screen()
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
			get_screen()
			click_change(get_xy('./imgs/models/sweep.png'))
			click_change((830,880))#点击关闭
			get_screen()
			click_change(get_xy('./imgs/models/return.png'))
	
	time.sleep(2)
	get_screen()
	click_change(get_xy('./imgs/models/home.png'))
	time.sleep(1)
	return#daily_challenge
