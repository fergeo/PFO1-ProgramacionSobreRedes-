#!/usr/bin/env python3
# client.py
"""
Cliente de chat simple:
- Se conecta a localhost:5000
- Envía múltiples mensajes hasta que el usuario escribe "éxito"
- Muestra la respuesta del servidor por cada mensaje enviado
"""

import socket
import sys

HOST = "127.0.0.1"
PORT = 5000
BUFFER_SIZE = 4096
ENCODING = "utf-8"


def run_client(host=HOST, port=PORT):
    """Bucle principal del cliente: conectar, enviar mensajes y mostrar respuestas."""
    try:
        # Configuración socket cliente TCP/IP
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        print(
            f"[INFO] Conectado a {host}:{port}. Escribe mensajes. Para terminar escribe: éxito"
        )
    except Exception as e:
        print(f"[ERROR] No se pudo conectar al servidor {host}:{port} — {e}")
        return

    try:
        with sock:
            while True:
                try:
                    mensaje = input("Mensaje: ")
                except (EOFError, KeyboardInterrupt):
                    print("\n[INFO] Terminando cliente.")
                    break

                if mensaje is None:
                    continue

                # Enviar el mensaje (incluimos también el caso en que el usuario escriba 'éxito')
                try:
                    sock.sendall(mensaje.encode(ENCODING))
                except Exception as e:
                    print(f"[ERROR] Error al enviar: {e}")
                    break

                # Leer respuesta del servidor
                try:
                    data = sock.recv(BUFFER_SIZE)
                    if not data:
                        print("[INFO] Servidor cerró la conexión.")
                        break
                    respuesta = data.decode(ENCODING)
                    print(f"Servidor: {respuesta}")
                except Exception as e:
                    print(f"[ERROR] Error al recibir respuesta: {e}")
                    break

                # Si el usuario escribió 'éxito' (exacto), terminamos el cliente
                if mensaje.strip().lower() == "éxito":
                    print("[INFO] 'éxito' recibido: cerrando conexión local.")
                    break

    except Exception as e:
        print(f"[ERROR] Excepción en el cliente: {e}")
    finally:
        try:
            sock.close()
        except:
            pass
        print("[INFO] Cliente finalizado.")


if __name__ == "__main__":
    run_client()
