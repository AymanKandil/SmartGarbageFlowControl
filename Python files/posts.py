import requests
import random
from datetime import datetime
import RPi.GPIO as GPIO
import time
import smtplib
from time import sleep
from sys import exit

from_email = 'Place Your email here'
recepients_list = ['Place recepients email here']
message = '''\
Subject: Trash Bin Full

Dear user,
          your trash bin is full, please empty it.
Thank you!'''
username = 'Place Your email here'
password = 'Place Your emails password here'
server = 'smtp.gmail.com:587'
n_emails = 0
def sendemail (from_addr, to_addr, message, login, password, smtpserver):
    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login, password)
    problems = server.sendmail(from_addr, to_addr, message)
    server.quit ()



GPIO.setmode (GPIO.BCM)

TRIG=23
ECHO=24

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.setup(22, GPIO.OUT)
p=GPIO.PWM(22,50)
p.start(0)
time.sleep(0.3)
p.ChangeDutyCycle(12)
time.sleep(0.3)
p.ChangeDutyCycle(0)
while True:
    try:
        count_hour=1
        count_reading=0
        sum_reading=0
        while (count_hour!=48):
            while (count_reading!=25):
                GPIO.output(TRIG,False)
                print ("waiting for sensor")
                time.sleep (0.1)
                #SOUND WAVE IS SENT
                GPIO.output(TRIG,True)
                time.sleep(0.00001)#10MICROSECONDS WAIT
                GPIO.output(TRIG,False)
                #WAITING FOR ECHO
                while GPIO.input(ECHO)==0:
                    pass
                pulse_start=time.time()
                #LISTEN/RECIVE SOUND WAVE
                while GPIO.input(ECHO)==1:
                    pass
                pulse_end=time.time()
                #TOTAL TIME
                pulse_duration = pulse_end - pulse_start
                #DISTANCE= TIME X SPEED
                distance = (pulse_duration* 17200)
                distance = round(distance,2)
                sum_reading= sum_reading + distance
                count_reading = count_reading+1
                time.sleep(0.1)
            print("done 25 readings")
            avg=sum_reading/25
            avg=round(avg)
            d_percent= 100-((avg/15.5)*100)
            d_percent= round(d_percent,2)
            r = requests.post("Place your add url here", data = { "distance_value": d_percent, "timestamp": datetime.now().timestamp() })
            if d_percent >=70:
                p.ChangeDutyCycle(4.5)
                time.sleep(0.5)
                p.ChangeDutyCycle(0)
                p.stop()
                sendemail(from_email, recepients_list, message, username, password, server)
                n_emails = n_emails + 1
                print("You have sent: " + str(n_emails) + " email(s).")
                sleep(1)
            count_hour= count_hour +1
            count_reading=0
            sum_reading=0
            time.sleep(30)#every 30 minss
    except KeyboardInterrupt:
        GPIO.cleanup()
        break

