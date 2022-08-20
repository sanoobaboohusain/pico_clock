
def convert_raw_temp_value(raw_value):
    conversion_factor = 3.3 / 65535
    reading = raw_value * conversion_factor
    temperature = 27 - (reading - 0.706) / 0.001721
    int_temp = int(temperature)
    return int_temp

