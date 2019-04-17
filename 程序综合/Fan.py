import RPi.GPIO as GPIO
import time, sys

motor_pin = 9;


def main():
	
	GPIO.setup(motor_pin, GPIO.OUT);

	motor = GPIO.PWM(motor_pin, 400)

	def myprint(msg):
		sys.stdout.write(msg+"\n");


	def changePower(power):
		motor.ChangeDutyCycle(0.002/(1.0/power*100))

	motor.start(0)

	#最高油门设定,这里最高油门的占空比是96
	motor.ChangeDutyCycle(96)
	#changePower(90)
	time.sleep(3);
	myprint("hight is finish");

	#最低油门设定 占空比30
	motor.ChangeDutyCycle(30)
	#changePower(10)
	time.sleep(6);

	#motor.ChangeDutyCycle(0)
	#changePower(10)
	#time.sleep(3);

	myprint("low is finish");

	#设定完毕，测试油门，一点一点增加
	for dc in range(20, 80, 1):
		motor.ChangeDutyCycle(dc)
		myprint("dc:"+str(dc))
		time.sleep(0.3);

	#time.sleep(10)
	motor.stop()