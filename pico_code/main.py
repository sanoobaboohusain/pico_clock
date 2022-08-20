from machine import Pin, ADC, PWM
import utime
import tm1637
import util

# initialise  all the external modules
led = Pin(25, Pin.OUT)
ldr = Pin(14, Pin.IN)
display = tm1637.TM1637(clk=Pin(0), dio=Pin(1))
temp_sensor_int = ADC(4)
buzzer = Pin(15, Pin.OUT)


# local variables


def main():
    int_temp_sensor_value = util.convert_raw_temp_value(temp_sensor_int.read_u16())
    display.temperature(int_temp_sensor_value)
    utime.sleep(2)


if __name__ == '__main__':
    while True:
        main()
