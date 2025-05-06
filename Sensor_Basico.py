import socket
import time

AGREGADOR_IP = '192.168.188.97'  # IP del agregador
AGREGADOR_PORT = 5001       
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
mensaje = "PING SENSOR 1"

# Enviar el mensaje al Agregador
while True:
    sock.sendto(mensaje.encode(), (AGREGADOR_IP, AGREGADOR_PORT))
    print(f"Mensaje '{mensaje}' enviado al Agregador ({AGREGADOR_IP}:{AGREGADOR_PORT})")
    time.sleep(2)  # Enviar un mensaje cada 2 segundos
