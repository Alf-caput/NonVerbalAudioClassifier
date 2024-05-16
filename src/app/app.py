import asyncio
import queue
import sys
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
import tensorflow as tf
# Define las variables de audio
device = 0  # ID del dispositivo de audio de forma predeterminada
window = 1000  # Ventana para los datos
downsample = 1  # Cuántas muestras descartar
channels = [1]  # Lista de canales de audio
interval = 30  # Intervalo de actualización en milisegundos para el gráfico

model = tf.keras.models.load_model("Conv1D_85.h5")
# Crea una cola
q = queue.Queue()
samplerate = 16000
seconds = 4
length = samplerate*seconds

# Creamos una variable para almacenar las muestras
plotdata = np.zeros((length, len(channels)))
pred = None

# Crea la figura y el eje de matplotlib
fig, ax = plt.subplots(figsize=(8, 4))
ax.set_facecolor((0, 0, 0))
ax.set_yticks([0])
ax.yaxis.grid(True)
ax.set_title("None")

# Crea una línea de color verde
lines = ax.plot(plotdata, color=(0, 1, 0.29))

# Función de devolución de llamada de audio para poner los datos en la cola
def audio_callback(indata, frames, time, status):
    q.put(indata[::downsample, [0]])

vocal_sounds = ['cough', 'laughter', 'sigh', 'sneeze', 'sniff', 'throatclearing']

interval = 0
# Función para actualizar el gráfico
def update_plot(frame):
    global plotdata
    global model
    global ax
    global interval
    global vocal_sounds
    while True:
        try:
            data = q.get_nowait()
        except queue.Empty:
            break
        shift = len(data)
        plotdata = np.roll(plotdata, -shift, axis=0)
        plotdata[-shift:, :] = data
        interval += shift
        print(interval)
        if interval > 16_000:
            interval = 0
            # ax.set_title(count)
            if np.abs(max(plotdata)) < 0.01:
                label = "None"
            else:
            
                pred = model.predict(np.expand_dims(plotdata, axis=0))
                idx = np.argmax(pred)
                label = vocal_sounds[idx]
            ax.set_title(label)
    for column, line in enumerate(lines):
        line.set_ydata(plotdata[:, column])
    return lines

# Configura el flujo de audio
stream = sd.InputStream(device=device, channels=max(channels), samplerate=samplerate, callback=audio_callback)

# Función principal
async def main():
    # Inicia el flujo de audio
    with stream:
        # Crea la animación
        ani = FuncAnimation(fig, update_plot, interval=interval, blit=False)
        # Ejecuta la operación de bloqueo de forma asíncrona
        # Muestra el gráfico
        plt.show()

# Ejecuta el bucle de eventos
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
