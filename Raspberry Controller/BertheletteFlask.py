#! /usr/bin/env python
#-*- coding: utf-8 -*-

import signal
import sys
import time
import os
import RPi.GPIO as GPIO
import json

from StepperMotor import StepperMotor
from ServoMotor import ServoMotor
from Solenoid import Solenoid
import _thread as thread  # for python 3   
import threading
from time import sleep

save_file_name = 'motors_save.json'

default_speed = 5

offset_low_speed = 17

SPEED_LIMIT = 50

motorA = StepperMotor(21,20,16,12,2,7*9,200, default_speed,-88)  
motorB = StepperMotor(26,19,13,6,2,7*7,200, default_speed,134)   
motorC = StepperMotor(18,15,14,23,2,7*7,200, default_speed,-106)
motorD = StepperMotor(22,27,17,4,2,7*7,200, default_speed,-142)
servoA = ServoMotor(7)
servoB = ServoMotor(8)
servoC = ServoMotor(9)
solenoid = Solenoid(11)

file_path = os.path.dirname(__file__)
sys.path.insert(0, file_path)

from flask import Flask, render_template, jsonify, Response, request,  send_file


app = Flask(__name__)

def initBerthelette():
    motorC.init_position(default_speed)
    motorB.init_position(default_speed)
    motorA.init_position(default_speed)
    motorD.init_position(default_speed)
    sleep(2)
    motorA.reach_angle_ramp(default_speed+17, default_speed, 1000, 0)
    motorD.reach_angle_ramp(default_speed+17,default_speed, 1000, -90)
    motorB.threaded_reach_angle_ramp(default_speed+17,default_speed, 1000, 0)
    motorC.threaded_reach_angle_ramp(default_speed+17,default_speed, 1000, 0)
    motorD.threaded_reach_angle_ramp(default_speed+17,default_speed, 1000, -90)
    

def syncronize_motor_speed(angleA, angleB, angleC, angleD):
    
    motors = [motorA, motorB, motorC, motorD]
    
    times = []
    
    times.append(motorA.get_angle_time(default_speed,angleA))
    times.append(motorB.get_angle_time(default_speed,angleB))
    times.append(motorC.get_angle_time(default_speed,angleC))
    times.append(motorD.get_angle_time(default_speed,angleD))
    longest_index = times.index(max(times))
    longest_time = times[longest_index]
    delayA = motorA.get_angle_delay(longest_time, angleA)
    delayB = motorB.get_angle_delay(longest_time, angleB)
    delayC = motorC.get_angle_delay(longest_time, angleC)
    delayD = motorD.get_angle_delay(longest_time, angleD)
    """
    
    times.append(motorA.get_ramp_angle_time(default_speed+17,default_speed, 1000, angleA))
    times.append(motorB.get_ramp_angle_time(default_speed+17,default_speed, 1000, angleB))
    times.append(motorC.get_ramp_angle_time(default_speed+17,default_speed, 1000, angleC))
    times.append(motorD.get_ramp_angle_time(default_speed+17,default_speed, 1000, angleD))
    longest_index = times.index(max(times))
    longest_time = times[longest_index]
    delayA = motorA.get_ramp_angle_delay(longest_time, angleA, 1000)
    delayB = motorB.get_ramp_angle_delay(longest_time, angleB, 1000)
    delayC = motorC.get_ramp_angle_delay(longest_time, angleC, 1000)
    delayD = motorD.get_ramp_angle_delay(longest_time, angleD, 1000)
    """
    delayA = delayA if delayA < SPEED_LIMIT else SPEED_LIMIT
    delayB = delayB if delayB < SPEED_LIMIT else SPEED_LIMIT
    delayC = delayC if delayC < SPEED_LIMIT else SPEED_LIMIT
    delayD = delayD if delayD < SPEED_LIMIT else SPEED_LIMIT
    print("delays: ")
    print(delayA, delayB, delayC, delayD)
    return delayA, delayB, delayC, delayD

@app.route('/openSolenoid', strict_slashes=False)
def openSolenoid():
    solenoid.open()
    listDic = {}
    listDic['SUCCESS'] = "Setpoint set"

    tmp = jsonify(listDic)
    tmp.headers['Access-Control-Allow-Origin'] = '*'
    return tmp
   
@app.route('/closeSolenoid', strict_slashes=False)
def closeSolenoid():
    solenoid.close()
    listDic = {}
    listDic['SUCCESS'] = "Setpoint set"

    tmp = jsonify(listDic)
    tmp.headers['Access-Control-Allow-Origin'] = '*'
    return tmp
    
@app.route('/init', strict_slashes=False)
def initRequest():
    initBerthelette()
    listDic = {}
    listDic['SUCCESS'] = "Setpoint set"

    tmp = jsonify(listDic)
    tmp.headers['Access-Control-Allow-Origin'] = '*'
    return tmp
  
@app.route('/initA', strict_slashes=False)  
def initARequest():
    motorA.init_position(default_speed)
    listDic = {}
    listDic['SUCCESS'] = "Setpoint set"

    tmp = jsonify(listDic)
    tmp.headers['Access-Control-Allow-Origin'] = '*'
    return tmp  
    
@app.route('/initB', strict_slashes=False)  
def initBRequest():
    motorB.init_position(default_speed)
    listDic = {}
    listDic['SUCCESS'] = "Setpoint set"

    tmp = jsonify(listDic)
    tmp.headers['Access-Control-Allow-Origin'] = '*'
    return tmp  
    
@app.route('/initC', strict_slashes=False)  
def initCRequest():
    motorC.init_position(default_speed)
    listDic = {}
    listDic['SUCCESS'] = "Setpoint set"

    tmp = jsonify(listDic)
    tmp.headers['Access-Control-Allow-Origin'] = '*'
    return tmp  
    
@app.route('/initD', strict_slashes=False)  
def initDRequest():
    motorD.init_position(default_speed)
    listDic = {}
    listDic['SUCCESS'] = "Setpoint set"

    tmp = jsonify(listDic)
    tmp.headers['Access-Control-Allow-Origin'] = '*'
    return tmp
    
@app.route('/angleA/<float(signed=True):angle>', strict_slashes=False)
def angleA(angle):
    motorA.threaded_reach_angle(default_speed, angle)
    listDic = {}
    listDic['SUCCESS'] = "Setpoint set"

    tmp = jsonify(listDic)
    tmp.headers['Access-Control-Allow-Origin'] = '*'
    return tmp

@app.route('/angleB/<float(signed=True):angle>', strict_slashes=False)
def angleB(angle):
    motorB.threaded_reach_angle(default_speed, angle)
    listDic = {}
    listDic['SUCCESS'] = "Setpoint set"

    tmp = jsonify(listDic)
    tmp.headers['Access-Control-Allow-Origin'] = '*'
    return tmp

@app.route('/angleC/<float(signed=True):angle>', strict_slashes=False)
def angleC(angle):
    motorC.threaded_reach_angle(default_speed, angle)
    listDic = {}
    listDic['SUCCESS'] = "Setpoint set"

    tmp = jsonify(listDic)
    tmp.headers['Access-Control-Allow-Origin'] = '*'
    return tmp

@app.route('/angleD/<float(signed=True):angle>', strict_slashes=False)
def angleD(angle):
    motorD.threaded_reach_angle(default_speed, angle)
    listDic = {}
    listDic['SUCCESS'] = "Setpoint set"

    tmp = jsonify(listDic)
    tmp.headers['Access-Control-Allow-Origin'] = '*'
    return tmp
    
@app.route('/angleAll/<float(signed=True):angleA>/<float(signed=True):angleB>/<float(signed=True):angleC>/<float(signed=True):angleD>', strict_slashes=False)
def angleAll(angleA,angleB,angleC,angleD):
    delayA, delayB, delayC, delayD = syncronize_motor_speed(angleA, angleB, angleC, angleD)
    
    motorA.threaded_reach_angle_ramp(delayA+17, delayA, 1000, angleA)
    motorB.threaded_reach_angle_ramp(delayB+17,delayB, 1000, angleB)
    motorC.threaded_reach_angle_ramp(delayC+17,delayC, 1000, angleC)
    motorD.threaded_reach_angle_ramp(delayD+17,delayD, 1000, angleD)
  
    listDic = {}
    listDic['SUCCESS'] = "Setpoint set"

    tmp = jsonify(listDic)
    tmp.headers['Access-Control-Allow-Origin'] = '*'
    return tmp
  
@app.route('/angleAllLonpoll/<float(signed=True):angleA>/<float(signed=True):angleB>/<float(signed=True):angleC>/<float(signed=True):angleD>/<float:servoAngleA>/<float:servoAngleB>/<float:servoAngleC>', strict_slashes=False)
def angleAllLonpoll(angleA,angleB,angleC,angleD, servoAngleA, servoAngleB, servoAngleC):
    delayA, delayB, delayC, delayD = syncronize_motor_speed(angleA, angleB, angleC, angleD)
    
    servoA.set_angle(servoAngleA)
    servoB.set_angle(servoAngleB)
    servoC.set_angle(servoAngleC)
    
    thread_angle_a = motorA.threaded_reach_angle_ramp(delayA+offset_low_speed, delayA, 1000, angleA)
    thread_angle_b = motorB.threaded_reach_angle_ramp(delayB+offset_low_speed,delayB, 1000, angleB)
    thread_angle_c = motorC.threaded_reach_angle_ramp(delayC+offset_low_speed,delayC, 1000, angleC)
    thread_angle_d = motorD.threaded_reach_angle_ramp(delayD+offset_low_speed,delayD, 1000, angleD)
    
    while(thread_angle_a.isAlive() == True or thread_angle_b.isAlive() == True or thread_angle_c.isAlive() == True or thread_angle_d.isAlive() == True):
        sleep(0.1)
  
    listDic = {}
    listDic['SUCCESS'] = "Setpoint set"

    tmp = jsonify(listDic)
    tmp.headers['Access-Control-Allow-Origin'] = '*'
    return tmp
    
@app.route('/servoA/<float:angle>', strict_slashes=False)
def servoARequest(angle):
    servoA.set_angle(angle)
    listDic = {}
    listDic['SUCCESS'] = "Setpoint set"

    tmp = jsonify(listDic)
    tmp.headers['Access-Control-Allow-Origin'] = '*'
    return tmp
    
@app.route('/servoB/<float:angle>', strict_slashes=False)
def servoBRequest(angle):
    servoB.set_angle(angle)
    listDic = {}
    listDic['SUCCESS'] = "Setpoint set"

    tmp = jsonify(listDic)
    tmp.headers['Access-Control-Allow-Origin'] = '*'
    return tmp
    
@app.route('/servoC/<float:angle>', strict_slashes=False)
def servoCRequest(angle):
    servoC.set_angle(angle)
    listDic = {}
    listDic['SUCCESS'] = "Setpoint set"

    tmp = jsonify(listDic)
    tmp.headers['Access-Control-Allow-Origin'] = '*'
    return tmp
    
@app.route('/servoAll/<float:angleA>/<float:angleB>/<float:angleC>', strict_slashes=False)
def servoAllRequest(angleA, angleB, angleC):
    servoA.set_angle(angleA)
    servoB.set_angle(angleB)
    servoC.set_angle(angleC)
    listDic = {}
    listDic['SUCCESS'] = "Setpoint set"

    tmp = jsonify(listDic)
    tmp.headers['Access-Control-Allow-Origin'] = '*'
    return tmp
    
def save_motors_json():
    data = {}
    data['motorA']= {
        'actual_step' : motorA.actual_step
    }
    data['motorB']= {
        'actual_step' : motorB.actual_step
    }
    data['motorC']= {
        'actual_step' : motorC.actual_step
    }
    data['motorD']= {
        'actual_step' : motorD.actual_step
    }
    with open(save_file_name, 'w') as outfile:
        json.dump(data, outfile)

def signal_handler(sig, frame):
    GPIO.cleanup()
    save_motors_json()
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    if os.path.exists(save_file_name):
        with open(save_file_name) as json_file:
            data = json.load(json_file)
            motorA.actual_step = data['motorA']['actual_step']
            motorB.actual_step = data['motorB']['actual_step']
            motorC.actual_step = data['motorC']['actual_step']
            motorD.actual_step = data['motorD']['actual_step']
    else:
        initBerthelette()
    app.run(host='::', debug=False, use_reloader=False)
