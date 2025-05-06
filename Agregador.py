import socket

from threading import Thread

# Inicializar reloj de Lamport y lista de eventos
lamport_clock = 0
eventos = []  # Lista de tuplas: (id_sensor, temp, t_remitente, lamport_clock)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 5001))

def handleClient(data, addr):
    global lamport_clock

    try:
        # Decodificar y separar los datos esperados en el mensaje
        mensaje = data.decode()
        id_sensor, temp, t_remitente = mensaje.split(",")
        temp = float(temp)
        t_remitente = int(t_remitente)

        # Regla 2b de Lamport
        lamport_clock = max(lamport_clock, t_remitente) + 1

        # Guardar el evento
        eventos.append((id_sensor, temp, t_remitente, lamport_clock))

        # Log detallado
        print(f"[TS:{lamport_clock}] Recibido T={temp:.1f}°C de {id_sensor} (TS_Sensor: {t_remitente})")

    except Exception as e:
        print(f"Error al procesar mensaje de {addr}: {e}")

print("Agregador escuchando en puerto 5001...")

while True:
    data, addr = sock.recvfrom(1024)
    thread = Thread(target=handleClient, args=(data, addr))
    thread.start()
