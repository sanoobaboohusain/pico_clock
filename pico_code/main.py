from machine import Pin, ADC, PWM
import utime
import _thread
import tm1637

led = Pin(25, Pin.OUT)
led_red = Pin(17, Pin.OUT)
led_green = Pin(16, Pin.OUT)

sw_1 = Pin(12, Pin.IN, Pin.PULL_DOWN)
sw_2 = Pin(13, Pin.IN, Pin.PULL_DOWN)

ldr = Pin(14, Pin.IN)

tm = tm1637.TM1637(clk=Pin(0), dio=Pin(1))
led_green.value(0)
led_red.value(0)
sensor_pin = ADC(4)
conversion_factor = 3.3 / (65535)
tm.brightness(2)

s_lock = _thread.allocate_lock()

tm.scroll('sound', delay=250)
utime.sleep(1)
tm.show('')
buzzer = PWM(Pin(15))

buzzer = Pin(15, Pin.OUT)


def beep():
    buzzer.value(1)
    utime.sleep(0.1)
    buzzer.value(0)


def sw_1_int_handler(pin):
    sw_1.irq(handler=None)
    beep()
    led_red.value(1)
    utime.sleep(1)
    led_red.value(0)
    led_green.value(1)
    utime.sleep(1)
    led_green.value(0)
    sw_1.irq(handler=sw_1_int_handler)


def sw_2_int_handler(pin):
    sw_2.irq(handler=None)
    beep()
    for i in range(20):
        led_red.value(1)
        utime.sleep(0.2)
        led_red.value(0)
        led_green.value(1)
        utime.sleep(0.2)
        led_green.value(0)
        sw_2.irq(handler=sw_2_int_handler)


def ldr_int_high(pin):
    ldr.irq(handler=None)
    tm.brightness(1)
    ldr.irq(handler=ldr_int_high)


def core_task():
    while True:
        s_lock.acquire()
        utime.sleep(1)
        led_red.value(1)
        utime.sleep(1)
        led_red.value(0)
        s_lock.release()


_thread.start_new_thread(core_task, ())

sw_1.irq(trigger=Pin.IRQ_RISING, handler=sw_1_int_handler)
sw_2.irq(trigger=Pin.IRQ_RISING, handler=sw_2_int_handler)
ldr.irq(trigger=Pin.IRQ_RISING, handler=ldr_int_high)


def read_and_update_temp():
    reading = sensor_pin.read_u16() * conversion_factor
    temperature = 27 - (reading - 0.706) / 0.001721
    int_temp = int(temperature)
    tm.temperature(int_temp)
    utime.sleep(1)


while True:
    s_lock.acquire()
    read_and_update_temp()
    if ldr.value() == 0:
        tm.brightness(7)
    s_lock.release()

