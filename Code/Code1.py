import machine
import time
import ustruct
#import matplotlib.pyplot as plt

uart = machine.UART(0, baudrate=9600, bits=16, parity=None, stop=1, tx=machine.Pin(0), rx=machine.Pin(1))

analog_in_values = []

for i in range(182):
    analog_in_values.append(machine.ADC(machine.Pin(26)).read_u16())
    time.sleep(0.0075)

msg = ustruct.pack('>182H', *analog_in_values)

uart.write(msg)

uart.write("Valores analógicos: " + str(analog_in_values))
print(str(analog_in_values))

#plt.plot(str(analog_in_values))
#plt.ylabel('some numbers')
#plt.show()
