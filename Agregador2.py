import socket
import signal
import sys
from threading import Thread

# Inicializar reloj de Lamport y lista de eventos
lamport_clock = 0
registros = []  # Lista persistente de eventos: (id_sensor, temp, t_remitente, lamport_clock)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 5001))

def handleClient(data, addr):
    global lamport_clock

    try:
        mensaje = data.decode()
        id_sensor, temp, t_remitente = mensaje.split(",")
        temp = float(temp)
        t_remitente = int(t_remitente)

        # Regla 2b de Lamport
        lamport_clock = max(lamport_clock, t_remitente) + 1

        # Guardar el evento
        registros.append((id_sensor, temp, t_remitente, lamport_clock))

        # Log detallado
        print(f"[TS:{lamport_clock}] Recibido T={temp:.1f}°C de {id_sensor} (TS_Sensor: {t_remitente})")

    except Exception as e:
        print(f"Error al procesar mensaje de {addr}: {e}")

def analizar_primer_umbral(registros, umbral):
    print("\n=== Análisis del primer evento que supera el umbral por sensor ===")
    
    # Filtrar eventos que superen el umbral
    filtrados = [r for r in registros if r[1] > umbral]

    if not filtrados:
        print(f"Ningún sensor superó el umbral de {umbral}°C.")
        return

    sensores = {}
    for r in filtrados:
        id_sensor, temp, t_remitente, lamport = r
        if id_sensor not in sensores or t_remitente < sensores[id_sensor][2]:
            sensores[id_sensor] = r  # Guardar el más temprano por t_remitente

    for id_sensor, (id_s, temp, t_remitente, lamport) in sensores.items():
        print(f"\nSensor {id_sensor} superó el umbral con {temp:.1f}°C")
        print(f"  → Timestamp lógico del sensor: {t_remitente}, Lamport local: {lamport}")

def cerrar_servidor(sig, frame):
    print("\n\nCerrando Agregador...")
    analizar_primer_umbral(registros, umbral=25.0)
    sock.close()
    sys.exit(0)

# Capturar Ctrl+C para cerrar correctamente
signal.signal(signal.SIGINT, cerrar_servidor)

print("Agregador escuchando en puerto 5001...")

while True:
    data, addr = sock.recvfrom(1024)
    thread = Thread(target=handleClient, args=(data, addr))
    thread.start()
