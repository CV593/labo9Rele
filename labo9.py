import tkinter as tk
from time import sleep
import serial
from serial.tools.list_ports import comports

estado_leds = [0, 0, 0]
ciclo_activo = False  
def setup_serial():
    global puerto
    puerto = serial.Serial(comports()[0].device, 9600)
    sleep(2)
def enviar_comando(comando):
    try:
        puerto.write(comando.encode())
    except serial.SerialException:
        print("Error de comunicación con Arduino")
        puerto.close()
def actualizar_semaforo(estado_leds):
    canvas.delete("LED")
    colores = ["green", "yellow", "red"]
    for i, estado in enumerate(estado_leds):
        color = colores[i] if estado else "black"
        x = 50 + i * 150
        canvas.create_oval(x, 100, x + 100, 200, fill=color, tags="LED")
def iniciar_ciclo():
    global ciclo_activo
    ciclo_activo = True
    while ciclo_activo:  
        enviar_comando('1')
        actualizar_semaforo([1, 0, 0])
        ventana.update()
        sleep(6)
        actualizar_semaforo([0, 1, 0])
        ventana.update()
        for _ in range(4):
            if not ciclo_activo:
                break
            actualizar_semaforo([0, 1, 0])
            ventana.update()
            sleep(0.2)
            actualizar_semaforo([0, 0, 0])
            ventana.update()
            sleep(0.2)
        if not ciclo_activo: 
            break
        actualizar_semaforo([0, 0, 1])
        ventana.update()
        sleep(5)
        actualizar_semaforo([0, 0, 0])
        enviar_comando('5')
def detener_ciclo():
    global ciclo_activo
    ciclo_activo = False  
def cerrar_puerto():
    puerto.close()

ventana = tk.Tk()
ventana.title("Semaforo")
canvas = tk.Canvas(ventana, width=800, height=300)
canvas.pack()
boton_inicio = tk.Button(ventana, text="Iniciar Ciclo", command=iniciar_ciclo)
boton_inicio.pack(side="left", padx=10, pady=10)
boton_detener = tk.Button(ventana, text="Detener Ciclo", command=detener_ciclo)
boton_detener.pack(side="left", padx=10, pady=10)
setup_serial()
actualizar_semaforo(estado_leds)
ventana.mainloop()
cerrar_puerto()
