from machine import Pin, ADC, ADCBlock

ADC_EN = Pin(14, Pin.OUT)

ADC_PIN = Pin(34)
# __ADC__ = ADC(ADC_PIN, atten=ADC.ATTN_11DB)
ADC_Block = ADCBlock(1, bits=12)
__ADC__ = ADC_Block.connect(ADC_PIN)
__ADC__.atten(ADC.ATTN_11DB)

CVF1 = 1.783

def get_volt(loop=20):
    global __ADC__
    global CVF1

    ADC_EN.value(1)
    adc_val = 0
    for _ in range(loop):
        adc_val += __ADC__.read()

    ADC_EN.value(0)
    adc_val = adc_val / loop
    volt = adc_val * CVF1 / 1000
    return volt


def get_charge_level(x):
    y = 100
    x2 = x*x
    x3 = x*x2
    if x <= 3.7:
        y = 6.763*x3-42.541*x2+67.665*x
    else:
        y = -233.99*x2+2022.2*x-4267.3

    return int(round(y))

