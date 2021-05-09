import RPi.GPIO as GPIO
from time import sleep
import threading

class ServoMotor:
    def __init__(self, SERVOPIN):    
        self.actual_angle = None
        self.SERVOPIN = SERVOPIN
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.SERVOPIN, GPIO.OUT)
        self.pwm=GPIO.PWM(self.SERVOPIN, 50)
        self.pwm.start(0)        
    def set_angle(self, angle):
        if angle != self.actual_angle:
            duty = angle / 18 + 2
            GPIO.output(self.SERVOPIN, True)
            self.pwm.ChangeDutyCycle(duty)
            sleep(.3)
            GPIO.output(self.SERVOPIN, False)
            self.pwm.ChangeDutyCycle(0)
        self.actual_angle = angle 
    def set_angle_hold(self, angle):
        if angle != self.actual_angle:
            duty = angle / 18 + 2
            GPIO.output(self.SERVOPIN, True)
            self.pwm.ChangeDutyCycle(duty)
        self.actual_angle = angle 
    def release(self):        
        GPIO.output(self.SERVOPIN, False)
        self.pwm.ChangeDutyCycle(0)
    def threaded_set_angle(self,angle):
        t = threading.Thread(target=self.set_angle, args=(angle,))
        t.start()
        return t
    def threaded_set_angle_hold(self,angle):
        t = threading.Thread(target=self.set_angle_hold, args=(angle,))
        t.start()
        return t

