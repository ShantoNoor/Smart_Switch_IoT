from machine import Pin, ADC

ADC_PIN = Pin(34)
__ADC__ = ADC(ADC_PIN, atten=ADC.ATTN_11DB)

CVF = 1.783


def get_volt(loop=50):
    global __ADC__
    global CVF

    adc_val = 0
    for _ in range(loop):
        adc_val += __ADC__.read()

    adc_val = adc_val / loop
    volt = adc_val * CVF / 1000
    return volt


def get_charge_level(x):
    x2 = x * x
    x3 = x * x2

    y = 100
    if x >= 4.2:
        return y

    if x <= 3.7:
        y = 6.763 * x3 - 42.541 * x2 + 67.665 * x
    else:
        y = -233.99 * x2 + 2022.2 * x - 4267.3

    return int(y)
