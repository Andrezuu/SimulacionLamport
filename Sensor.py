import socket
import time
import random

# Configuración del sensor
AGREGADOR_IP = '127.0.0.1'  # IP del agregador
AGREGADOR_PORT = 5001
ID_SENSOR = "S1"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

lamport_clock = 0  # Reloj de Lamport local

while True:
    # ===== Evento: Lectura de temperatura =====
    lamport_clock += 1  # Regla 1: evento interno
    temperatura = round(random.uniform(20.0, 30.0), 1)  # Simula una lectura
    print(f"[TS:{lamport_clock}] Sensor {ID_SENSOR} leyó T={temperatura:.1f}°C")

    # ===== Evento: Envío de mensaje =====
    lamport_clock += 1  # Regla 1: evento de envío
    t_envio = lamport_clock

    mensaje = f"{ID_SENSOR},{temperatura},{t_envio}"
    sock.sendto(mensaje.encode(), (AGREGADOR_IP, AGREGADOR_PORT))
    print(f"[TS:{t_envio}] Enviando lectura T={temperatura:.1f}°C")

    time.sleep(2)  # Espera 2 segundos antes de la próxima lectura
