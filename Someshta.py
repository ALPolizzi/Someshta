
# coding: utf-8

# In[5]:



import time
print(time.localtime())


# In[9]:


#import picamera
import time
from datetime import datetime
#import ads1x15.py
import gpiozero
from cryptography.fernet import Fernet
#Global Variables
RUNNING = True
lastMeasure = time.clock_gettime(time.CLOCK_REALTIME)

measureRate = 1000
photoRate = 60000

f_Ph = 0
v_Ph = 0

camera = picamera.PiCamera()
camera.resolution = (3280, 2464)

with open("callandor.key", "rb") as filekey:
    key = filekey.read()
fernet = Fernet(key)

#Device declaration
adc = ADS1115(i2c, address = 72, gain = 0) #gain = 0 -> 5v in ADC, 3.3v out to Pi

#REPL
while RUNNING:
    if (time.clock_gettime(time.CLOCK_REALTIME) - lastMeasure) > measureRate:
        f_Ph = adc.read(rate = 0, channel1 = 0)
        v_Ph = adc.read(rate = 0, channel1 = 1)
        lastMeasure = time.clock_gettime(time.CLOCK_REALTIME)
        #write to file
        #encrypt
    if (time.clock_gettime(time.CLOCK_REALTIME) - lastPhoto) > photoRate:
        camera.start_preview()
        sleep(2)
        s_now = datetime.now().isoformat()
        camera.capture('timelapse/'+s_now+".jpg")
        with open('timelapse/'+s_now+".jpg", "rb") as file:
            clear_pic = file.read()
        enc_pic = fernet.encrypt(clear_pic)
        with open('timelapse/'+s_now+".jpg", "wb") as enc_file:
            enc_file.write(enc_pic)

