
from machine import Pin, ADC, PWM, RTC
import utime
import tm1637
import util

# initialise  all the external modules
led = Pin(25, Pin.OUT)
ldr = Pin(14, Pin.IN)
display = tm1637.TM1637(clk=Pin(0), dio=Pin(1))
temp_sensor_int = ADC(4)
buzzer = Pin(15, Pin.OUT)
rtc = RTC()

# local variables


def set_rtc():
    rtc.datetime((2022, 8, 23, 2, 12, 48, 0, 0))


def display_temperature():
    int_temp_sensor_value = util.convert_raw_temp_value(temp_sensor_int.read_u16())
    display.temperature(int_temp_sensor_value)
    utime.sleep(2)


def clear_display():
    display.write([0, 0, 0, 0])


def show_time():
    colon_flag = True
    while True:
        number = [12, 34]
        display.numbers(number[0], number[1], colon_flag)
        colon_flag = not colon_flag
        utime.sleep(1)


def main():
    set_rtc()
    show_time()


if __name__ == '__main__':
    main()
