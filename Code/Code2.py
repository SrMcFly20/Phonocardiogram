 
import machine
import rp2
import utime
import uasyncio as asyncio

# Configurar el pin GPIO 26 como entrada analógica
adc = machine.ADC(26)

# Configurar la interrupción para leer los datos a 5 kHz
@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW)
def adc_read():
    set(pins, 1)               # Establecer el pin en alto
    nop()                      # Esperar 2 ciclos de reloj
    nop()
    read(nob, 0)               # Leer el dato y almacenarlo en nob
    set(pins, 0)               # Establecer el pin en bajo
    nop()                      # Esperar 2 ciclos de reloj
    nop()
    mov(isr, nob)              # Mover nob al registro isr
    push()                     # Guardar el registro isr en la pila
    irq(rel(0))                # Generar una interrupción para repetir el bucle

# Configurar la frecuencia de la interrupción
sm = rp2.StateMachine(0, adc_read, freq=5000, sideset_base=machine.Pin(26))

# Configurar la comunicación serial a través del puerto USB
uart = machine.UART(0, baudrate=115200)

async def main():
    while True:
        # Generar un buffer de 1000 muestras
        buffer = b''
        for i in range(1000):
            # Esperar a que se complete la lectura del ADC
            while not sm.rx_fifo:
                pass

            # Leer una muestra de la entrada analógica
            data = sm.get()

            # Imprimir el dato leído en la consola
            print("Dato leído:", data)

            # Convertir el dato de 16 bits en un buffer de bytes
            buffer += data.to_bytes(2, byteorder='little')

        # Enviar el buffer a través del puerto USB
        uart.write(buffer)

        # Esperar 1 segundo antes de enviar el siguiente conjunto de datos
        await asyncio.sleep(1)

# Ejecutar el bucle principal de asyncio
asyncio.run(main())