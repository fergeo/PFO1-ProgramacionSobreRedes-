#!/usr/bin/env python3
# server.py
"""
Servidor de chat básico:
- Escucha en localhost:5000
- Acepta conexiones concurrentes (threads)
- Guarda cada mensaje en SQLite con campos: id, contenido, fecha_envio, ip_cliente
- Responde al cliente con: "Mensaje recibido: <timestamp>"
"""

import socket
import threading
import sqlite3
from datetime import datetime
import sys
import traceback

DB_FILE = "messages.db"
HOST = "127.0.0.1"
PORT = 5000
BACKLOG = 5
BUFFER_SIZE = 4096
ENCODING = "utf-8"


# ---------------------------
# Base de datos
# ---------------------------
def init_db(db_file=DB_FILE):
    """Inicializa la base de datos SQLite y crea la tabla si no existe."""
    try:
        conn = sqlite3.connect(db_file, check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contenido TEXT NOT NULL,
                fecha_envio TEXT NOT NULL,
                ip_cliente TEXT NOT NULL
            )
        """
        )
        conn.commit()
        return conn
    except Exception as e:
        print(f"[ERROR DB] No se pudo inicializar la DB: {e}")
        raise


def save_message(db_conn, contenido, fecha_envio, ip_cliente):
    """Guarda un mensaje en la tabla messages."""
    try:
        cursor = db_conn.cursor()
        cursor.execute(
            "INSERT INTO messages (contenido, fecha_envio, ip_cliente) VALUES (?, ?, ?)",
            (contenido, fecha_envio, ip_cliente),
        )
        db_conn.commit()
    except Exception as e:
        print(f"[ERROR DB] Error al guardar mensaje: {e}")
        # No propagamos el error al cliente, pero lo registramos
        traceback.print_exc()


# ---------------------------
# Sockets: inicialización y aceptación
# ---------------------------
def init_socket(host=HOST, port=PORT):
    """Configura y devuelve un socket TCP listo para aceptar conexiones."""
    try:
        # Configuración del socket TCP/IP
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Permite reutilizar la dirección inmediatamente después de cerrar (útil en desarrollo)
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((host, port))
        server_sock.listen(BACKLOG)
        print(f"[INFO] Servidor escuchando en {host}:{port}")
        return server_sock
    except OSError as e:
        # Manejo de error típico: puerto ocupado
        print(f"[ERROR SOCKET] No se pudo iniciar el socket en {host}:{port} — {e}")
        raise


def handle_client(conn, addr, db_conn):
    """
    Función que corre en un hilo por cada cliente:
    - Recibe mensajes (protocolo simple: cada recv se interpreta como un mensaje)
    - Guarda mensaje en DB
    - Responde con timestamp
    """
    cliente_ip = addr[0]
    print(f"[INFO] Conexión aceptada de {cliente_ip}:{addr[1]}")
    try:
        with conn:
            while True:
                data = conn.recv(BUFFER_SIZE)
                if not data:
                    # cliente cerró la conexión
                    print(f"[INFO] Cliente {cliente_ip} desconectado.")
                    break

                try:
                    mensaje = data.decode(ENCODING).strip()
                except UnicodeDecodeError:
                    print("[WARN] Mensaje con encoding inválido recibido; se ignorará.")
                    continue

                if mensaje == "":
                    # mensaje vacío: ignorar
                    continue

                # timestamp en formato ISO local
                timestamp = datetime.now().isoformat(sep=" ", timespec="seconds")

                # Guardar en DB
                try:
                    save_message(db_conn, mensaje, timestamp, cliente_ip)
                    print(
                        f"[DB] Guardado mensaje de {cliente_ip} a las {timestamp}: {mensaje}"
                    )
                except Exception as e:
                    print(f"[ERROR] Al guardar en DB: {e}")

                # Responder al cliente
                respuesta = f"Mensaje recibido: {timestamp}"
                try:
                    conn.sendall(respuesta.encode(ENCODING))
                except Exception as e:
                    print(f"[ERROR] No se pudo enviar la respuesta a {cliente_ip}: {e}")
                    break
    except Exception as e:
        print(f"[ERROR] En manejo de cliente {cliente_ip}: {e}")
        traceback.print_exc()


def accept_connections(server_sock, db_conn):
    """Bucle principal que acepta conexiones y lanza un hilo por cliente."""
    try:
        while True:
            conn, addr = server_sock.accept()
            client_thread = threading.Thread(
                target=handle_client, args=(conn, addr, db_conn), daemon=True
            )
            client_thread.start()
    except KeyboardInterrupt:
        print("\n[INFO] Servidor detenido por teclado.")
    except Exception as e:
        print(f"[ERROR] Error en accept loop: {e}")
        traceback.print_exc()
    finally:
        try:
            server_sock.close()
        except:
            pass


# ---------------------------
# Main
# ---------------------------
def main():
    # Inicializar DB
    try:
        db_conn = init_db()
    except Exception:
        print("[FATAL] Imposible inicializar la DB. Saliendo.")
        sys.exit(1)

    # Inicializar socket
    try:
        server_sock = init_socket()
    except Exception:
        print("[FATAL] Imposible iniciar el socket. Saliendo.")
        sys.exit(1)

    # Aceptar conexiones
    accept_connections(server_sock, db_conn)


if __name__ == "__main__":
    main()
