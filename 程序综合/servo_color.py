#-*- coding:UTF-8 -*-
import RPi.GPIO as GPIO
import TCS3200
import time
import numpy as np

# 设置电机信号端口
Servo_180 = 11

#设置GPIO口为BCM编码方式
GPIO.setmode(GPIO.BCM)

#忽略警告信息
GPIO.setwarnings(False)
def main():
    # 180电机初始化程序
    def servo180_init():
        global pwm_servo
        GPIO.setup(Servo_180, GPIO.OUT)
        #设置pwm引脚和频率为50hz
        pwm_servo = GPIO.PWM(Servo_180, 50)
        pwm_servo.start(0)

    #电机PWM更新函数
    def servo180_update():
        for pos in range(181):
            pwm_servo.ChangeDutyCycle(2.5 + 10 * pos/180)
        time.sleep(0.009)
        #for pos in reversed(range(181)):
            #pwm_servo.ChangeDutyCycle(2.5 + 10 * pos/180)
        #time.sleep(0.009)

    #Servo Turn Contorl
    def servo180_turn_contorl(direction):
        if direction == 1:
            #for pos in range(90,180):
                pwm_servo.ChangeDutyCycle(2.5 + 10 * 180/180)
                #print pos
                time.sleep(1)
            #for pos in reversed(range(90,180)):
                pwm_servo.ChangeDutyCycle(2.5 + 10 * 90/180)
                #print pos
                time.sleep(1)
        if direction == 0:
            #for pos in reversed(range(0,90)):
                pwm_servo.ChangeDutyCycle(2.5 + 10 * 0/180)
                #print pos
                time.sleep(1)
            #for pos in range(0,90):
                pwm_servo.ChangeDutyCycle(2.5 + 10 * 90/180)
                #print pos
                time.sleep(1)
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
    #try/except语句用来检测try语句块中的错误，
    #从而让except语句捕获异常信息并处理。
    flag = True

    # TCS3200初始化
    setup()

    # 舵机初始化
    servo180_init()


    while flag:
        try:
            # 舵机初始化向前
            pwm_servo.ChangeDutyCycle(2.5 + 10 * 90/180)
            time.sleep(1)

            # 获取当前检测到的颜色值
            value = get_Median_RGB()
            target = "red"
            get_color = print_which_color(value)
            
            # 判断检到的颜色是否为目标颜色
            # 如果是红色就正转
            if get_color  == "none":
                pass
            elif get_color == target:
                servo180_turn_contorl(1)
                print("电机正转")

            # 如果是其他颜色反转
            else:
                servo180_turn_contorl(0)      
                print("电机反转")


        except KeyboardInterrupt:
            pass
    pwm_servo.stop()
    GPIO.cleanup()
