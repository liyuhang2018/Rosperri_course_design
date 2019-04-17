#-*- coding:UTF-8 -*-
import RPi.GPIO as GPIO
import time
import numpy as np

# 设置TCS3200端口
s2 = 20
s3 = 21
signal = 16

NUM_CYCLES = 10
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# 端口初始化
def setup():
	GPIO.setup(signal, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(s2, GPIO.OUT )
	GPIO.setup(s3, GPIO.OUT )
	print "\n"

# 采集实时RGB值
def loop():
	temp = 1
	while  True:
		GPIO.output(s2,GPIO.LOW)
		GPIO.output(s3,GPIO.LOW)
		time.sleep(0.05)

		start = time.time()
		for impulse_count in range (NUM_CYCLES):
			GPIO.wait_for_edge(signal, GPIO.FALLING)
		duration = time.time() - start #seconds to run for loop
		red = NUM_CYCLES / duration #in Hz
		#print "red value - ",red
		GPIO.output(s2,GPIO.LOW)
		GPIO.output(s3,GPIO.HIGH)
		time.sleep(0.05)

		start = time.time()
		for impulse_count in range (NUM_CYCLES):
			GPIO.wait_for_edge(signal, GPIO.FALLING)
		duration = time.time() - start #seconds to run for loop
		blue = NUM_CYCLES / duration #in Hz
		#print "blue value - ",blue
		GPIO.output(s2,GPIO.HIGH)
		GPIO.output(s3,GPIO.HIGH)
		time.sleep(0.05)

		start = time.time()
		for impulse_count in range (NUM_CYCLES):
			GPIO.wait_for_edge(signal, GPIO.FALLING)
		duration = time.time() - start #seconds to run for loop
		green = NUM_CYCLES / duration #in Hz
		#print "green value - ",green
		#print "***********************************************"
		time.sleep(0.05)
		return red, green, blue

# 获取9次检测后的中值
def get_Median_RGB():
    redlist = list()
    greenlist = list()
    bluelist = list()
    for i in range(5):
        red , green, blue = loop()
        redlist.append(red)
        greenlist.append(green)
        bluelist.append(blue)
    redlist = np.array(redlist)
    greenlist = np.array(greenlist)
    bluelist = np.array(bluelist)
    data = [np.median(redlist),np.median(greenlist), np.median(bluelist)]
    print 'data', data
    return data

# 打印TCS3200检测结果
def print_which_color(a):

    # 设置想采集标准色值
    print("采集red球")

    color_red = "red"
    COLOR_red = np.array([13023.650680028633, 6900.303308221422, 8500.737991266375])
    None_ = np.array([8300, 5300, 6000])
    # y = np.array(['white', 'green', 'red', 'blue'])
    a = np.array(a)

    # 计算当前检测值和COLOR的距离
    distance = np.linalg.norm(a-COLOR_red)
    distance_none = np.linalg.norm(a-None_)

    # 取距离绝对值
    distance_abs = np.abs(distance)
    distance_none_abs = np.abs(distance_none)
    print "distance_abs", distance_abs
    print "distance_none_abs", distance_none_abs

    # 设定距离阈值
    if distance_none_abs  < 3000:
        print "None"
        none = "none"
        return none

    elif distance_abs < 1500:
        print("是目标颜色")
        return color_red
    else:
        print("不是目标颜色")
        return 0

# 清除端口占用
def endprogram():
        GPIO.cleanup()


# 检测程序用，测试时注释掉
# if __name__=='__main__':
#    setup()
#     try:  	
#         value = get_Median_RGB()
#         target = "red"
#         print_which_color(value)

#     except KeyboardInterrupt:
#         endprogram()

