from multiprocessing import Process
import RPi.GPIO as GPIO
import time
import numpy as np
import Ultrasonic
import servo_color
def init():
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)


def main():
	init()

	p1 = Process(target = Ultrasonic.main)
	p2 = Process(target = servo_color.main)
	p3 = Process(target = Fan.main)
	p1.start()
	p2.start()
	p3.start()



if __name__ == '__main__':
	main()