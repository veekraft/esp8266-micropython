from machine import Pin, Signal

ledP=4
buttonP=5

led=Signal(ledP,Pin.OUT,invert=False)
button=Pin(buttonP,Pin.IN,Pin.PULL_UP)

while True:
    if button.value()==0:           # if button is pressed
        led.on()                    # turn on led
        print ('led turned on >>>') # print information on terminal
    else :                          # if button is relessed
        led.off()                   # turn off led 
        print ('led turned off <<<')    
