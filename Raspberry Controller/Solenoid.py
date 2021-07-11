import RPi.GPIO as GPIO
from time import sleep
import signal
import sys
import threading

class Solenoid:
    def __init__(self, SOLENOID_PIN):        
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTSTP, self.signal_handler)
        GPIO.setmode(GPIO.BCM)
        self.SOLENOID_PIN = SOLENOID_PIN
        GPIO.setup(self.SOLENOID_PIN, GPIO.OUT)
        GPIO.output(self.SOLENOID_PIN, GPIO.LOW)
        self.closing_thread = None
        
    def signal_handler(self, sig, frame):
        self.reset_all()        
        close()
        print("Solenoid class exited properly, GPIO reset in safe state")
        sys.exit(0)
        
    def open(self):
        GPIO.output(self.SOLENOID_PIN, GPIO.HIGH)
        if self.closing_thread == None or self.closing_thread.is_alive() == False:
            self.closing_thread = threading.Timer(5, self.__differed_close)
            self.closing_thread.start()
            print("start")
    
    def close(self):
        GPIO.output(self.SOLENOID_PIN, GPIO.LOW)
        if self.closing_thread != None:
            self.closing_thread.cancel()
        
    def __differed_close(self):
        GPIO.output(self.SOLENOID_PIN, GPIO.LOW)


