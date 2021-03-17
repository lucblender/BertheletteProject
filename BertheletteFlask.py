#! /usr/bin/env python
#-*- coding: utf-8 -*-

import signal
import sys
import time
import os
import RPi.GPIO as GPIO

from StepperMotor import StepperMotor
from ServoMotor import ServoMotor
import _thread as thread  # for python 3   
import threading
from time import sleep

default_speed = 5

SPEED_LIMIT = 30

motorA = StepperMotor(21,20,16,12,2,7*9,200, default_speed,-88)  
motorB = StepperMotor(26,19,13,6,2,7*7,200, default_speed,134)   
motorC = StepperMotor(18,15,14,23,2,7*7,200, default_speed,-106)
motorD = StepperMotor(22,27,17,4,2,7*7,200, default_speed,-142)
servoA = ServoMotor(7)
servoB = ServoMotor(8)
servoC = ServoMotor(9)

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
    motorA.reach_angle(default_speed,0)
    motorD.reach_angle(default_speed,-90)
    motorB.threaded_reach_angle(default_speed,0)
    motorC.threaded_reach_angle(default_speed,0)

    #motorA.threaded_reach_setpoint(10)
    #motorB.threaded_reach_setpoint(10)
    #motorC.threaded_reach_setpoint(7)
    #motorD.threaded_reach_setpoint(7,-90)
    

def syncronize_motor_speed(angleA, angleB, angleC, angleD):
    
    motors = [motorA, motorB, motorC, motorD]
    
    times = []
    times.append(motorA.get_angle_time(default_speed,angleA))
    times.append(motorB.get_angle_time(default_speed,angleB))
    times.append(motorC.get_angle_time(default_speed,angleC))
    times.append(motorD.get_angle_time(default_speed,angleD))
    print("times:")
    for time in times:
        print(time)
    longest_index = times.index(max(times))
    longest_time = times[longest_index]
    print("longest index: ", longest_index, "longest time: ", longest_time)
    delayA = motorA.get_angle_delay(longest_time, angleA)
    delayB = motorB.get_angle_delay(longest_time, angleB)
    delayC = motorC.get_angle_delay(longest_time, angleC)
    delayD = motorD.get_angle_delay(longest_time, angleD)
    
    delayA = delayA if delayA < SPEED_LIMIT else SPEED_LIMIT
    delayB = delayB if delayB < SPEED_LIMIT else SPEED_LIMIT
    delayC = delayC if delayC < SPEED_LIMIT else SPEED_LIMIT
    delayD = delayD if delayD < SPEED_LIMIT else SPEED_LIMIT
    print("delays: ")
    print(delayA, delayB, delayC, delayD)
    return delayA, delayB, delayC, delayD



    
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
    motorA.threaded_reach_angle(10, angle)
    print(angle)
    listDic = {}
    listDic['SUCCESS'] = "Setpoint set"

    tmp = jsonify(listDic)
    tmp.headers['Access-Control-Allow-Origin'] = '*'
    return tmp

@app.route('/angleB/<float(signed=True):angle>', strict_slashes=False)
def angleB(angle):
    motorB.threaded_reach_angle(10, angle)
    print(angle)
    listDic = {}
    listDic['SUCCESS'] = "Setpoint set"

    tmp = jsonify(listDic)
    tmp.headers['Access-Control-Allow-Origin'] = '*'
    return tmp

@app.route('/angleC/<float(signed=True):angle>', strict_slashes=False)
def angleC(angle):
    motorC.threaded_reach_angle(7, angle)
    print(angle)
    listDic = {}
    listDic['SUCCESS'] = "Setpoint set"

    tmp = jsonify(listDic)
    tmp.headers['Access-Control-Allow-Origin'] = '*'
    return tmp

@app.route('/angleD/<float(signed=True):angle>', strict_slashes=False)
def angleD(angle):
    motorD.threaded_reach_angle(7, angle)
    print(angle)
    listDic = {}
    listDic['SUCCESS'] = "Setpoint set"

    tmp = jsonify(listDic)
    tmp.headers['Access-Control-Allow-Origin'] = '*'
    return tmp
    
@app.route('/angleAll/<float(signed=True):angleA>/<float(signed=True):angleB>/<float(signed=True):angleC>/<float(signed=True):angleD>', strict_slashes=False)
def angleAll(angleA,angleB,angleC,angleD):
    delayA, delayB, delayC, delayD = syncronize_motor_speed(angleA, angleB, angleC, angleD)
    #motorA.threaded_reach_angle(delayA, angleA)
    #motorB.threaded_reach_angle(delayB, angleB)
    #motorC.threaded_reach_angle(delayC, angleC)
    #motorD.threaded_reach_angle(delayD, angleD)
    
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
    
    servoA.threaded_set_angle(servoAngleA)
    servoB.threaded_set_angle(servoAngleB)
    servoC.threaded_set_angle(servoAngleC)
    
    thread_angle_a = motorA.threaded_reach_angle_ramp(delayA+17, delayA, 1000, angleA)
    thread_angle_b = motorB.threaded_reach_angle_ramp(delayB+17,delayB, 1000, angleB)
    thread_angle_c = motorC.threaded_reach_angle_ramp(delayC+17,delayC, 1000, angleC)
    thread_angle_d = motorD.threaded_reach_angle_ramp(delayD+17,delayD, 1000, angleD)
    
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
    print(angle)
    listDic = {}
    listDic['SUCCESS'] = "Setpoint set"

    tmp = jsonify(listDic)
    tmp.headers['Access-Control-Allow-Origin'] = '*'
    return tmp
    
@app.route('/servoB/<float:angle>', strict_slashes=False)
def servoBRequest(angle):
    servoB.set_angle(angle)
    print(angle)
    listDic = {}
    listDic['SUCCESS'] = "Setpoint set"

    tmp = jsonify(listDic)
    tmp.headers['Access-Control-Allow-Origin'] = '*'
    return tmp
    
@app.route('/servoC/<float:angle>', strict_slashes=False)
def servoCRequest(angle):
    servoC.set_angle(angle)
    print(angle)
    listDic = {}
    listDic['SUCCESS'] = "Setpoint set"

    tmp = jsonify(listDic)
    tmp.headers['Access-Control-Allow-Origin'] = '*'
    return tmp
    
@app.route('/servoAll/<float:angleA>/<float:angleB>/<float:angleC>', strict_slashes=False)
def servoAllRequest(angleA, angleB, angleC):
    servoA.threaded_set_angle(angleA)
    servoB.threaded_set_angle(angleB)
    servoC.threaded_set_angle(angleC)
    listDic = {}
    listDic['SUCCESS'] = "Setpoint set"

    tmp = jsonify(listDic)
    tmp.headers['Access-Control-Allow-Origin'] = '*'
    return tmp
    
def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    initBerthelette()
    app.run(host='::', debug=False, use_reloader=False)
