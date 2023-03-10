from machine import UART,Timer
from fpioa_manager import fm
from Maix import GPIO

import sensor,lcd,time,utime,image
import KPU as kpu
import uos

#Function module part
###############
#clear 1
###############
def clear():
    lcd.draw_string(0, 0, "               ",lcd.WHITE, lcd.WHITE)
    lcd.draw_string(0, 10, "              ",lcd.WHITE, lcd.WHITE)
    lcd.draw_string(0, 20, "              ",lcd.WHITE, lcd.WHITE)
    utime.sleep_ms(10)
    lcd.draw_string(0, 30, "              ",lcd.WHITE, lcd.WHITE)
    lcd.draw_string(0, 40, "              ",lcd.WHITE, lcd.WHITE)
    lcd.draw_string(0, 50, "              ",lcd.WHITE, lcd.WHITE)
    utime.sleep_ms(10)
    lcd.draw_string(0, 60, "              ",lcd.WHITE, lcd.WHITE)
    lcd.draw_string(0, 70, "              ",lcd.WHITE, lcd.WHITE)
    lcd.draw_string(0, 80, "              ",lcd.WHITE, lcd.WHITE)
    utime.sleep_ms(10)
    lcd.draw_string(0, 90, "              ",lcd.WHITE, lcd.WHITE)
    lcd.draw_string(0, 100, "              ",lcd.WHITE, lcd.WHITE)
    lcd.draw_string(0, 110, "              ",lcd.WHITE, lcd.WHITE)
    utime.sleep_ms(10)
    lcd.draw_string(0, 120, "              ",lcd.WHITE, lcd.WHITE)
    lcd.draw_string(0, 130, "              ",lcd.WHITE, lcd.WHITE)
    lcd.draw_string(0, 140, "              ",lcd.WHITE, lcd.WHITE)
    utime.sleep_ms(10)
    lcd.draw_string(0, 150, "              ",lcd.WHITE, lcd.WHITE)
    lcd.draw_string(0, 160, "              ",lcd.WHITE, lcd.WHITE)
    lcd.draw_string(0, 170, "              ",lcd.WHITE, lcd.WHITE)
    lcd.draw_string(0, 180, "              ",lcd.WHITE, lcd.WHITE)
    utime.sleep_ms(10)

###############
#clear 2
###############
def clear2():

    lcd.draw_string(0, 100, "              ",lcd.WHITE, lcd.WHITE)
    lcd.draw_string(0, 110, "              ",lcd.WHITE, lcd.WHITE)
    utime.sleep_ms(10)
    lcd.draw_string(0, 120, "              ",lcd.WHITE, lcd.WHITE)
    lcd.draw_string(0, 130, "              ",lcd.WHITE, lcd.WHITE)
    lcd.draw_string(0, 140, "              ",lcd.WHITE, lcd.WHITE)
    utime.sleep_ms(10)
    lcd.draw_string(0, 150, "              ",lcd.WHITE, lcd.WHITE)
    lcd.draw_string(0, 160, "              ",lcd.WHITE, lcd.WHITE)
    lcd.draw_string(0, 170, "              ",lcd.WHITE, lcd.WHITE)
    lcd.draw_string(0, 180, "              ",lcd.WHITE, lcd.WHITE)
    utime.sleep_ms(10)
###############
#Initialization function
###############
def all_init():
    fm.register(12, fm.fpioa.GPIO0)#Map pins and initializations

    fm.register(10, fm.fpioa.GPIOHS10)
    fm.register(11, fm.fpioa.GPIOHS11)

    fm.register(9, fm.fpioa.GPIOHS9)
    fm.register(18, fm.fpioa.GPIOHS18)
    fm.register(19, fm.fpioa.GPIOHS19)
    fm.register(20, fm.fpioa.GPIOHS20)

    global LED1   #PIN10
    global BEER   #PIN11

    global DOOR   #PIN9
    global MQ3    #PIN18
    global BUTTON #PIN19
    global KEY    #PIN20

    global BUTTON_state
    BUTTON_state=0

    global LED_B

    global clock
    LED_B = GPIO(GPIO.GPIO0, GPIO.OUT,value=1)

    LED1   = GPIO(GPIO.GPIOHS10, GPIO.OUT,value=0)
    BEER   = GPIO(GPIO.GPIOHS11, GPIO.OUT,value=1)

    DOOR   = GPIO(GPIO.GPIOHS9,GPIO.IN,GPIO.PULL_UP)
    MQ3    = GPIO(GPIO.GPIOHS18,GPIO.IN,GPIO.PULL_UP)
    BUTTON = GPIO(GPIO.GPIOHS19,GPIO.IN,GPIO.PULL_UP)
    KEY    = GPIO(GPIO.GPIOHS20,GPIO.IN,GPIO.PULL_UP)

    clock = time.clock()
    #init the camera
    sensor.reset()
    #sensor.set_vflip(1)
    sensor.set_pixformat(sensor.RGB565)
    sensor.set_framesize(sensor.QVGA)
    sensor.skip_frames(time = 2000)     # Wait for the Settings to take effect
    clock = time.clock()

#############
#Face recognition initialization
#############
def face_init():
    global task
    task = kpu.load("/sd/facedetect.kmodel")
    anchor = (1.889, 2.5245, 2.9465, 3.94056, 3.99987, 5.3658, 5.155437, 6.92275, 6.718375, 9.01025)
    a = kpu.init_yolo2(task, 0.1, 0.3, 5, anchor)

#############
#Face recognition judgment
#############
def face_judgment():
    clock.tick()
    img = sensor.snapshot()
    code = kpu.run_yolo2(task, img) #??????yolo2??????
    global peopleNum
    peopleNum=0
    global flag2
    global people
    if not code is None:
       peopleNum=int(code[0].objnum())#????????????
       print(peopleNum)
       if(peopleNum==1 and flag2 == 1):
        flag2 = 0
        people = 1

#############
#The buzzer 
#############
def beer_control(n):
    if n == 1:
        BEER.value(0)
    if n == 0:
        BEER.value(1)

#############
#LED indicating lamp
#############
def LED_control(n):
    if n == 1:
        LED1.value(1)
    if n == 0:
        LED1.value(0)

#############
#Initialize the LCD display
#############
def LCD_init():
    #lcd.init()
    lcd.init()
    lcd.freq(10000000)
    lcd.clear(lcd.WHITE)
    lcd.rotation(1) #?????????????????????240*320????????????????????????90??
    lcd.display(image.Image("demo1.bmp"))   #??????
    utime.sleep_ms(20)
    lcd.draw_string(210, 120, "  ",lcd.WHITE, lcd.RED) #??????
    lcd.draw_string(175,120, "  ",lcd.WHITE, lcd.RED) #??????
    lcd.draw_string(145, 120, "  ",lcd.WHITE, lcd.RED) #??????
    #lcd.draw_string(53, 120, "  ",lcd.WHITE,lcd.RED) #??????



#############
#LCD????????????
#############
def LCD_control():
    global flag1
    global BUTTON_state
    clock.tick()
    img = sensor.snapshot()         # ???????????????????????????.
    lcd.rotation(2)
    lcd.display(img,roi = (100,100,120,150),oft=(200,50)) # ???LCD?????????

    lcd.draw_string(270, 218, str(peopleNum),lcd.BLACK, lcd.WHITE) #??????
    lcd.rotation(1)

    if peopleNum==1:
        lcd.draw_string(145, 120, "  ",lcd.WHITE, lcd.BLUE)#??????
        while(flag1):
            beer_control(1)
            utime.sleep_ms(200)
            beer_control(0)
            flag1 = 0
    if flag1 == 0 and peopleNum<2:
        lcd.draw_string(145, 120, "  ",lcd.WHITE, lcd.BLUE)#??????

    if peopleNum>1:
        lcd.draw_string(145, 120, "  ",lcd.WHITE, lcd.YELLOW)#??????

    if BUTTON.value()==0:
        if MQ3.value()==1:
            lcd.draw_string(210, 120, "  ",lcd.WHITE, lcd.BLUE) #??????
            BUTTON_state=1
        if MQ3.value()==0:
            lcd.draw_string(210, 120, "  ",lcd.WHITE, lcd.RED) #??????
            lcd.display(image.Image("demo8.bmp"),roi = (0,0,105,195),oft=(0,0))#??????
            beer_control(1)
            utime.sleep(1.5)
            beer_control(0)
            lcd.display(image.Image("demo1.bmp"),roi = (0,0,105,195),oft=(0,0))#??????
    if DOOR.value()==0:
        lcd.draw_string(175,120, "  ",lcd.WHITE, lcd.BLUE) #??????
    if DOOR.value()==1:
        lcd.draw_string(175,120, "  ",lcd.WHITE, lcd.RED) #??????
#############
#??????????????????
#############
def car__control():
    global BUTTON_state
    global people
    global flag3
    #?????????????????????????????????
    if people==1 and DOOR.value()==0 and BUTTON_state==1 and MQ3.value()==1 and KEY.value()==1:
        lcd.display(image.Image("demo2.bmp"),roi = (0,0,105,100),oft=(0,0))#??????
        utime.sleep_ms(500)
        LED1.value(0)

    #????????????????????????????????????????????????
    if people==1 and DOOR.value()==1 and BUTTON_state==1 and MQ3.value()==1 and KEY.value()==1:
        clear() #??????
        LED1.value(0)
        utime.sleep_ms(20)

    #????????????
    if KEY.value()==0 :
        #??????????????????????????????
        if people==1 and DOOR.value()==0 and BUTTON_state==1 and MQ3.value()==0:
            lcd.display(image.Image("demo8.bmp"),roi = (0,0,105,195),oft=(0,0))#??????
            utime.sleep_ms(10)
            lcd.draw_string(210, 120, "  ",lcd.WHITE, lcd.RED) #??????
            while KEY.value()==0 and people==1 and DOOR.value()==0 and BUTTON_state==1 and MQ3.value()==0:
                LED1.value(1)
                utime.sleep_ms(300)
                LED1.value(0)
                utime.sleep_ms(300)
            lcd.draw_string(210, 120, "  ",lcd.WHITE, lcd.BLUE) #??????
            clear() #??????
            lcd.display(image.Image("demo2.bmp"),roi = (0,0,105,100),oft=(0,0))#??????
        #??????????????????
        if people==1 and DOOR.value()==0 and BUTTON_state==1 and MQ3.value()==1 :
           utime.sleep_ms(30)
           LED1.value(1)
           flag3 = 0
        if flag3 == 0 and DOOR.value()==1 :
            lcd.clear()
            while(True):
                LED1.value(0)

        #??????????????????
    if people==0  or DOOR.value()==1 or BUTTON_state==0:
        if KEY.value()==0 :
            lcd.display(image.Image("demo3.bmp"),roi = (40,10,70,65),oft=(40,0))#??????
            utime.sleep_ms(20)
            if people==0:
                lcd.display(image.Image("demo5.bmp"),roi = (65,65,20,120),oft=(65,70))#??????
                utime.sleep_ms(20)
            else:
                lcd.rotation(0)#??????
                lcd.draw_string(135, 70, "              ",lcd.WHITE, lcd.WHITE)#??????
                lcd.draw_string(135, 65, "              ",lcd.WHITE, lcd.WHITE)#??????
                lcd.rotation(1)
            if DOOR.value()==1:
                utime.sleep_ms(20)
                lcd.display(image.Image("demo6.bmp"),roi = (40,70,20,120),oft=(45,70))#??????
                flag3 = 1
                utime.sleep_ms(20)
            else:
                lcd.rotation(0)#??????
                lcd.draw_string(135, 50, "              ",lcd.WHITE, lcd.WHITE)#??????
                lcd.draw_string(135, 46, "              ",lcd.WHITE, lcd.WHITE)#??????
                lcd.rotation(1)
                flag3 = 1
                utime.sleep_ms(20)
            if BUTTON_state==0:
                lcd.display(image.Image("demo4.bmp"),roi = (85,70,20,80),oft=(85,70))#??????
                utime.sleep_ms(20)
            else:
                lcd.rotation(0)#??????
                lcd.draw_string(136, 93, "              ",lcd.WHITE, lcd.WHITE)#??????
                lcd.draw_string(136, 85, "              ",lcd.WHITE, lcd.WHITE)#??????
                lcd.rotation(1)

            if KEY.value()==1 :

                clear() #??????
                utime.sleep_ms(20)
                clear() #??????
                utime.sleep_ms(20)
                LED1.value(0)

    if KEY.value()==1 :
        clear2() #??????
        utime.sleep_ms(20)
        clear2() #??????
        utime.sleep_ms(20)
        LED1.value(0)
    flag3 = 1
#############
#???????????????
#############
global flag1
flag1 = 1

global flag2
flag2 = 1
global flag3
flag3 = 1
global people
people = 0;
all_init()
face_init()
LCD_init()

while(True):
    face_judgment()
    LCD_control()
    car__control()

