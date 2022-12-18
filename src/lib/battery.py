from machine import Pin, ADC

ADC_EN = Pin(14, Pin.OUT)
ADC_PIN = Pin(34, Pin.IN)

adc = ADC(ADC_PIN)


def get_volt(loop=20):
    ADC_EN.on()

    val = 0
    for _ in range(loop):
        val += adc.read_u16()

    val = val / loop

    val = (val / 65535) * 2 * 3.3 * 1.1

    ADC_EN.off()

    return (val, (adc.read_uv() / 10 ** 6))
