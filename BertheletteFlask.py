#! /usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import time
import os

from StepperMotor import StepperMotor
from ServoMotor import ServoMotor
import _thread as thread  # for python 3   
import threading
from time import sleep

SPEED_LIMIT = 30

motorA = StepperMotor(21,20,16,12,1,7*9,200, 10,-88)  
motorB = StepperMotor(26,19,13,6,1,7*7,200, 7,134)   
motorC = StepperMotor(18,15,14,23,1,7*7,200, 7,-106)
motorD = StepperMotor(22,27,17,4,16,4,200, 7,-142)
servoA = ServoMotor(7)
servoB = ServoMotor(8)
servoC = ServoMotor(9)

file_path = os.path.dirname(__file__)
sys.path.insert(0, file_path)

from flask import Flask, render_template, jsonify, Response, request,  send_file


app = Flask(__name__)

def initBerthelette():
    motorC.init_position(7)
    motorB.init_position(7)
    motorA.init_position(10)
    motorD.init_position(7)

    sleep(2)

    motorA.reach_angle(10,0)
    motorD.reach_angle(7,-90)
    motorB.threaded_reach_angle(7,0)
    motorC.threaded_reach_angle(7,0)

    sleep(10)

    motorA.threaded_reach_setpoint(10)
    motorB.threaded_reach_setpoint(7)
    motorC.threaded_reach_setpoint(7)
    motorD.threaded_reach_setpoint(7,-90)
    

def syncronize_motor_speed(angleA, angleB, angleC, angleD):
    
    motors = [motorA, motorB, motorC, motorD]
    
    times = []
    times.append(motorA.get_angle_time(10,angleA))
    times.append(motorB.get_angle_time(7,angleB))
    times.append(motorC.get_angle_time(7,angleC))
    times.append(motorD.get_angle_time(7,angleD))
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
    
@app.route('/angleA/<float(signed=True):angle>', strict_slashes=False)
def angleA(angle):
    motorA.set_setpoint(angle)
    print(angle)
    listDic = {}
    listDic['SUCCESS'] = "Setpoint set"

    tmp = jsonify(listDic)
    tmp.headers['Access-Control-Allow-Origin'] = '*'
    return tmp

@app.route('/angleB/<float(signed=True):angle>', strict_slashes=False)
def angleB(angle):
    motorB.set_setpoint(angle)
    print(angle)
    listDic = {}
    listDic['SUCCESS'] = "Setpoint set"

    tmp = jsonify(listDic)
    tmp.headers['Access-Control-Allow-Origin'] = '*'
    return tmp

@app.route('/angleC/<float(signed=True):angle>', strict_slashes=False)
def angleC(angle):
    motorC.set_setpoint(angle)
    print(angle)
    listDic = {}
    listDic['SUCCESS'] = "Setpoint set"

    tmp = jsonify(listDic)
    tmp.headers['Access-Control-Allow-Origin'] = '*'
    return tmp

@app.route('/angleD/<float(signed=True):angle>', strict_slashes=False)
def angleD(angle):
    motorD.set_setpoint(angle)
    print(angle)
    listDic = {}
    listDic['SUCCESS'] = "Setpoint set"

    tmp = jsonify(listDic)
    tmp.headers['Access-Control-Allow-Origin'] = '*'
    return tmp
    
@app.route('/angleAll/<float(signed=True):angleA>/<float(signed=True):angleB>/<float(signed=True):angleC>/<float(signed=True):angleD>', strict_slashes=False)
def angleAll(angleA,angleB,angleC,angleD):
    delayA, delayB, delayC, delayD = syncronize_motor_speed(angleA, angleB, angleC, angleD)
    motorA.set_setpoint(angleA, delayA)
    motorB.set_setpoint(angleB, delayB)
    motorC.set_setpoint(angleC, delayC)
    motorD.set_setpoint(angleD, delayD)
    
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
    

from logging import FileHandler, Formatter, DEBUG

if __name__ == '__main__':
    initBerthelette()
    app.run(host='::', debug=False, use_reloader=False)
