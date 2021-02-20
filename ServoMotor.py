import RPi.GPIO as GPIO
from time import sleep

class ServoMotor:
    def __init__(self, SERVOPIN):    
        self.SERVOPIN = SERVOPIN
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.SERVOPIN, GPIO.OUT)
        self.pwm=GPIO.PWM(self.SERVOPIN, 50)
        self.pwm.start(0)
    def set_angle(self, angle):
        duty = angle / 18 + 2
        GPIO.output(self.SERVOPIN, True)
        self.pwm.ChangeDutyCycle(duty)
        sleep(1)
        GPIO.output(self.SERVOPIN, False)
        self.pwm.ChangeDutyCycle(0)
    def set_angle_hold(self, angle):
        duty = angle / 18 + 2
        GPIO.output(self.SERVOPIN, True)
        self.pwm.ChangeDutyCycle(duty)
    def release(self):        
        GPIO.output(self.SERVOPIN, False)
        self.pwm.ChangeDutyCycle(0)
