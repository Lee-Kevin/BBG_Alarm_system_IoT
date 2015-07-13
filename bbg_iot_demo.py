#  sodu pip install requests
# This is a demo by Kevin Lee
import requests
import time
import Adafruit_BMP.BMP085 as BMP085
from Adafruit_I2C import Adafruit_I2C
import bbg_grove_oled
import Adafruit_BBIO.GPIO as GPIO
from sendmail import alertMe

dweetIO = "https://dweet.io/dweet/for/"
myName = "BBG_IoT_Demo"
myKey = "Temperature"

sensor = BMP085.BMP085()
alertTime = 0 
alertFlag = 0               # no Alert
led    = "P9_21"            # UART2_TXD P9_21
GPIO.setup(led,GPIO.OUT)   

Button = "P9_22"            # UART2_RXD P9_22
GPIO.setup(Button, GPIO.IN)
GPIO.add_event_detect(Button, GPIO.FALLING)


def ButtonFunction(void):
    global alertFlag
    print "ButtonFunction"
    if alertFlag == 0:
        alertFlag = 1
        alertTime = time.time()+60
        GPIO.output(led,GPIO.LOW)
        
GPIO.add_event_callback(Button,ButtonFunction)             # regist the button interrupt function

if __name__=="__main__":
    
    bbg_grove_oled.oled_init()
    bbg_grove_oled.oled_setNormalDisplay()
    bbg_grove_oled.oled_clearDisplay()
    while True:
        # GPIO.output(led,GPIO.HIGH)
        # time.sleep(1)
        # GPIO.output(led,GPIO.LOW)
        # time.sleep(1)
        # print 'led'
        temperature = sensor.read_temperature()
        pressure    = sensor.read_pressure()
        altitude    = sensor.read_altitude()
        
        bbg_grove_oled.oled_setTextXY(0,0)
        bbg_grove_oled.oled_putString('Temp:{0:0.1f} *C'.format(temperature))
        bbg_grove_oled.oled_setTextXY(1,0)
        bbg_grove_oled.oled_putString('Pressure:')
        bbg_grove_oled.oled_setTextXY(2,0)
        bbg_grove_oled.oled_putString('  {0:0.1f} Kpa'.format(pressure/1000))
        bbg_grove_oled.oled_setTextXY(3,0)
        bbg_grove_oled.oled_putString('altitude:')
        bbg_grove_oled.oled_setTextXY(4,0)
        bbg_grove_oled.oled_putString('  {0:0.1f} m'.format(altitude))
        bbg_grove_oled.oled_setTextXY(5,0)
        bbg_grove_oled.oled_putString("SeeedStudio")

        print 'Temp \n {0:0.2f} *C'.format(temperature)
        print 'Pressure \n {0:0.2f} Pa'.format(pressure)
        print 'Altitude \n {0:0.2f} m'.format(altitude)
        print 'Sealevel Pressure = {0:0.2f} Pa'.format(sensor.read_sealevel_pressure())
        
        rqsString = dweetIO + myName + '?' + myKey + '=' + '{0:0.1f} '.format(temperature)
        # +'/' +  myKey + '=' + '{0:0.1f} *C'.format(sensor.read_temperature())
        # rqsString = dweetIO + myName + '?' + "{'Temperatuer':'23C','ADC':'123'}"
        print rqsString
        rqs = requests.get(rqsString)
        print rqs.status_code
        print rqs.headers
        print rqs.content
        if temperature >= 30 :
            if alertFlag == 0:                   # there is no alert before
                GPIO.output(led,GPIO.HIGH)
                if alertTime == 0:
                    alertTime = time.time() + 60
                    print "Temperature is too high. Alerting in 60 seconds if still high"
                else :
                    if time.time() > alertTime:
                        alertMe("Alert","The temperature is too high now")
                        alertTime = 0
                        print "send the alert email"
            elif alertFlag == 1:                #there is an alert but no effect
                if time.time() > alertTime:
                    alertFlag = 0
        else:
            alertFlag = 0
            GPIO.output(led,GPIO.LOW)
        time.sleep(10)