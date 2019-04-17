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
    
#try/except语句用来检测try语句块中的错误，
#从而让except语句捕获异常信息并处理。
flag = True

# TCS3200初始化
TCS3200.setup()

# 舵机初始化
servo180_init()


while  flag:
    try:
        # 舵机初始化向前
        pwm_servo.ChangeDutyCycle(2.5 + 10 * 90/180)
        time.sleep(1)

        # 获取当前检测到的颜色值
        value = TCS3200.get_Median_RGB()
        target = "red"
        get_color = TCS3200.print_which_color(value)
        
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
