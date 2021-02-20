import RPi.GPIO as GPIO
from time import sleep
import _thread as thread  # for python 3
import threading


class StepperMotor:
    def __init__(self, EN, DIR, STEP, LIMITSWITCH, step_ratio, gear_ratio, step_per_turn,origin_angle):
        self.EN_PIN = EN
        self.DIR_PIN = DIR
        self.STEP_PIN = STEP
        self.LIMITSWITCH_PIN = LIMITSWITCH
        self.step_ratio = step_ratio
        self.gear_ratio = gear_ratio
        self.step_per_turn = step_per_turn
        self.origin_angle = origin_angle
        self.actual_angle = 0
        self.actual_step = 0
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.EN_PIN, GPIO.OUT)
        GPIO.setup(self.DIR_PIN, GPIO.OUT)
        GPIO.setup(self.STEP_PIN, GPIO.OUT)
        GPIO.output(self.EN_PIN, GPIO.LOW)
        GPIO.output(self.DIR_PIN, GPIO.LOW)
        GPIO.setup(self.LIMITSWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    def init_position(self,delay=1):
        if self.origin_angle > 0:
            GPIO.output(self.DIR_PIN, GPIO.LOW)
        else:
            GPIO.output(self.DIR_PIN, GPIO.HIGH)
        sleep(0.1)
        while(GPIO.input(self.LIMITSWITCH_PIN) == 1):
            GPIO.output(self.STEP_PIN, GPIO.HIGH)
            sleep(0.0001)
            GPIO.output(self.STEP_PIN, GPIO.LOW)
            sleep(0.0001*delay) 
        self.actual_angle = self.origin_angle
        self.actual_step = 0
    def testramp0(self,delay_start=1, delay_stop=1, acceleration_time=1, step_ration=1):
        acceleration_time_s =  acceleration_time/1000
        cycle_average = (0.0001*delay_start+0.0001*delay_stop)
        ramp_cycles = (acceleration_time_s/cycle_average)
        increment = (delay_start-delay_stop)/ramp_cycles
        step_number = int(200*16*step_ration)
        GPIO.output(self.DIR_PIN, GPIO.LOW)
        sleep(0.1)    
        if ramp_cycles*2 > step_number:
            ramp_cycles = step_number/2
        for i in range(0,step_number):
        
            if i >= 0 and i < ramp_cycles:
                delay = delay_start-(i*increment)
            elif i >= ramp_cycles and i < (step_number - ramp_cycles):
                delay = delay_stop
            else :
                delay = delay_stop+((i-(step_number - ramp_cycles))*increment)
                
            GPIO.output(self.STEP_PIN, GPIO.HIGH)
            sleep(0.0001)
            GPIO.output(self.STEP_PIN, GPIO.LOW)
            sleep(0.0001*(delay))              
    def testramp1(self,delay_start=1, delay_stop=1, acceleration_time=1, step_ration=1):
        acceleration_time_s =  acceleration_time/1000
        cycle_average = (0.0001*delay_start+0.0001*delay_stop)
        ramp_cycles = (acceleration_time_s/cycle_average)
        increment = (delay_start-delay_stop)/ramp_cycles
        step_number = int(200*16*step_ration)  
        GPIO.output(self.DIR_PIN, GPIO.HIGH)
        sleep(0.1)  
        if ramp_cycles*2 > step_number:
            ramp_cycles = step_number/2
        for i in range(0,step_number):
        
            if i >= 0 and i < ramp_cycles:
                delay = delay_start-(i*increment)
            elif i >= ramp_cycles and i < (step_number - ramp_cycles):
                delay = delay_stop
            else :
                delay = delay_stop+((i-(step_number - ramp_cycles))*increment)
                
            GPIO.output(self.STEP_PIN, GPIO.HIGH)
            sleep(0.0001)
            GPIO.output(self.STEP_PIN, GPIO.LOW)
            sleep(0.0001*(delay))
            
    def rotation_angle(self,delay,degree,direction):
        if direction == 0:
            GPIO.output(self.DIR_PIN, GPIO.LOW)
            incr_step = +1
        else:
            GPIO.output(self.DIR_PIN, GPIO.HIGH)
            incr_step = -1
            
        step_number = int(((self.step_ratio*self.gear_ratio*self.step_per_turn)/360)*degree)
        
        sleep(0.1)
        for i in range(0,step_number):
            GPIO.output(self.STEP_PIN, GPIO.HIGH)
            sleep(0.0001)
            GPIO.output(self.STEP_PIN, GPIO.LOW)
            sleep(0.0001*delay)   
            self.actual_step += incr_step
            
    def reach_angle(self,delay=5,angle=0):
        actual_angle = ((((self.actual_step/self.gear_ratio)/self.step_ratio)/self.step_per_turn)*360)+self.origin_angle
        angle_to_do = actual_angle - angle
        if angle_to_do < 0:
            direction = 0
        else:
            direction = 1
        self.rotation_angle(delay,abs(angle_to_do),direction)

    def threaded_reach_angle(self,delay=5,angle=0):
        t = threading.Thread(target=self.reach_angle, args=(delay,angle))
        t.start()
        
        
        
        
        