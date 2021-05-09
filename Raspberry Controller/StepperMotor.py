import RPi.GPIO as GPIO
from time import sleep
import _thread as thread  # for python 3
import threading
import copy


class StepperMotor:
    def __init__(self, EN, DIR, STEP, LIMITSWITCH, step_ratio, gear_ratio, step_per_turn, default_delay, origin_angle):
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
        self.__setpoint = 0
        self.__setpoint_delay = 0
        self.default_delay = default_delay
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
          
    def rotation_angle_ramp(self,delay_start, delay_stop, acceleration_time_ms, angle, direction):
        if direction == 0:
            GPIO.output(self.DIR_PIN, GPIO.LOW)
            incr_step = +1
        else:
            GPIO.output(self.DIR_PIN, GPIO.HIGH)
            incr_step = -1
        
        step_number = self.get_step_number(angle)
        
        acceleration_time_s =  acceleration_time_ms/1000
        cycle_average = (0.0001*delay_start+0.0001*delay_stop)
        ramp_cycles = (acceleration_time_s/cycle_average)
        increment = (delay_start-delay_stop)/ramp_cycles
        sleep(0.1)  
        if ramp_cycles*2 > step_number:
            ramp_cycles = step_number/2
        for i in range(0,step_number):
            if (GPIO.input(self.LIMITSWITCH_PIN) == 0) and ((abs(self.get_actual_angle() - self.origin_angle))>10):
                print("limit switch in rotation_angle")
                return False
        
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
            self.actual_step += incr_step   
            
    def rotation_angle(self,delay,angle,direction,setpoint_break=False):
        local_setpoint_old = self.__setpoint
            
        if direction == 0:
            GPIO.output(self.DIR_PIN, GPIO.LOW)
            incr_step = +1
        else:
            GPIO.output(self.DIR_PIN, GPIO.HIGH)
            incr_step = -1
            
        step_number = self.get_step_number(angle)
        
        sleep(0.1)
        for i in range(0,step_number):
            if (GPIO.input(self.LIMITSWITCH_PIN) == 0) and ((abs(self.get_actual_angle() - self.origin_angle))>10):
                print("limit switch in rotation_angle")
                return False
            GPIO.output(self.STEP_PIN, GPIO.HIGH)
            sleep(0.0001)
            GPIO.output(self.STEP_PIN, GPIO.LOW)
            sleep(0.0001*delay)   
            self.actual_step += incr_step    
            if local_setpoint_old != self.__setpoint and setpoint_break == True:
                print("Break of rotation_angle")
                return False     
            local_setpoint_old = self.__setpoint
        return True
    
    def compute_angle_todo(self, angle):
        if angle > abs(self.origin_angle):
            angle = abs(self.origin_angle)
        elif angle < -abs(self.origin_angle):
            angle = -abs(self.origin_angle)
            
        actual_angle = self.get_actual_angle()
        angle_to_do = actual_angle - angle
        if angle_to_do < 0:
            direction = 0
        else:
            direction = 1
        return abs(angle_to_do),direction    
            
    def reach_angle(self,delay, angle):
        angle_to_do, direction = self.compute_angle_todo(angle)
        self.rotation_angle(delay,angle_to_do,direction)
            
    def reach_angle_ramp(self,delay_start, delay_stop, acceleration_time_ms, angle):
        angle_to_do, direction = self.compute_angle_todo(angle)
        self.rotation_angle_ramp(delay_start, delay_stop, acceleration_time_ms,angle_to_do,direction)

    def threaded_reach_angle(self, delay, angle):
        t = threading.Thread(target=self.reach_angle, args=(delay,angle))
        t.start()
        return t
            
    def threaded_reach_angle_ramp(self, delay_start, delay_stop, acceleration_time_ms, angle):
        t = threading.Thread(target=self.reach_angle_ramp, args=(delay_start, delay_stop, acceleration_time_ms, angle))
        t.start()
        return t
        
    def reach_setpoint(self):
        setpoint_old = None
        while(True):
            if self.__setpoint > abs(self.origin_angle):
                self.__setpoint = abs(self.origin_angle)
            elif self.__setpoint < -abs(self.origin_angle):
                self.__setpoint = -abs(self.origin_angle)
            reached = True
            if setpoint_old != self.__setpoint:
                setpoint_old = self.__setpoint
                actual_angle = self.get_actual_angle()
                angle_to_do = actual_angle - self.__setpoint
                if angle_to_do < 0:
                    direction = 0
                else:
                    direction = 1             
                reached = self.rotation_angle(self.__setpoint_delay,abs(angle_to_do),direction,True)
            if reached == True:
                setpoint_old = self.__setpoint
            sleep(0.01)
    
    def get_actual_angle(self):
        return ((((self.actual_step/self.gear_ratio)/self.step_ratio)/self.step_per_turn)*360)+self.origin_angle
    
    def get_step_number(self,angle):
        return int(((self.step_ratio*self.gear_ratio*self.step_per_turn)/360)*angle)
    
    def get_angle_time(self,delay,angle):
        real_angle = abs(self.get_actual_angle()-angle)
        return self.get_step_number(real_angle)*(0.0001+0.0001*(delay))
    
    def get_angle_delay(self,time,angle):
        real_angle = abs(self.get_actual_angle()-angle)
        if int(real_angle) == 0:
            return self.__setpoint_delay
        else:            
            return  ((time/self.get_step_number(real_angle))-0.0001)/0.0001
    
    def threaded_reach_setpoint(self,delay=5,setpoint=0):
        self.set_setpoint(setpoint)
        self.__setpoint_delay = delay
        t = threading.Thread(target=self.reach_setpoint, args=())
        t.start()
        return t
        
    def set_setpoint(self, setpoint, delay=0):
        if delay != 0:
            self.__setpoint_delay = delay
        else:
            self.__setpoint_delay = self.default_delay
        self.__setpoint = setpoint
        
        
        
        