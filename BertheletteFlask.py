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

motorA = StepperMotor(21,20,16,12,1,7*9,200,-88)  
motorB = StepperMotor(26,19,13,6,1,7*7,200,134)   
motorC = StepperMotor(18,15,14,23,1,7*7,200,-106)
motorD = StepperMotor(22,27,17,4,16,4,200,-142)
servoA = ServoMotor(7)
servoB = ServoMotor(8)
servoC = ServoMotor(9)

file_path = os.path.dirname(__file__)
sys.path.insert(0, file_path)

from flask import Flask, render_template, jsonify, Response, request,  send_file


app = Flask(__name__)

def initBerthelette():
    motorC.init_position(5)
    motorB.init_position(5)
    motorA.init_position(5)
    motorD.init_position(5)

    sleep(2)

    motorA.reach_angle(5,0)
    motorD.reach_angle(5,-90)
    motorB.threaded_reach_angle(5,0)
    motorC.threaded_reach_angle(5,0)

    sleep(10)

    motorA.threaded_reach_setpoint(7)
    motorB.threaded_reach_setpoint(7)
    motorC.threaded_reach_setpoint(7)
    motorD.threaded_reach_setpoint(7,-90)

    
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
    motorA.set_setpoint(angleA)
    motorB.set_setpoint(angleB)
    motorC.set_setpoint(angleC)
    motorD.set_setpoint(angleD)
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
