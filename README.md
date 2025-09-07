# Propuesta Formativa Obligatoria (PFO)

**TP: Implementación de un Chat Básico Cliente-Servidor con Sockets y Base de Datos**

## 📌 Objetivo

Aprender a configurar un servidor de sockets en Python que reciba mensajes de clientes,  
los almacene en una base de datos y envíe confirmaciones, aplicando buenas prácticas de  
modularización y manejo de errores.

---

## 🖥️ Tecnologías utilizadas

- Python 3.x
- Módulo `socket` (para la comunicación cliente-servidor)
- Módulo `sqlite3` (para persistencia de mensajes en base de datos)
- Programación concurrente con `threading`

---

## 📂 Estructura del proyecto

```
├── client.py      # Cliente de chat
├── server.py      # Servidor de chat
├── messages.db    # Base de datos SQLite (se genera automáticamente)
└── README.md      # Documentación del proyecto
```

---

## ⚙️ Configuración y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/fergeo/PFO1-ProgramacionSobreRedes-.git
cd PFO1-ProgramacionSobreRedes-
```

### 2. Ejecutar el servidor

En una terminal:

```bash
python server.py
```

El servidor quedará escuchando en `localhost:5000`.

### 3. Ejecutar el cliente

En otra terminal:

```bash
python client.py
```

Ahora podrás escribir mensajes desde el cliente.  
Cada mensaje será guardado en la base de datos y el servidor responderá con:

```
Mensaje recibido: <timestamp>
```

Para finalizar el cliente, escribe:

```
éxito
```

---

## 🗄️ Base de datos

El servidor genera automáticamente el archivo `messages.db` con la tabla:

```sql
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    contenido TEXT NOT NULL,
    fecha_envio TEXT NOT NULL,
    ip_cliente TEXT NOT NULL
);
```

### Consultar mensajes guardados

Ejecuta en terminal:

```bash
sqlite3 messages.db
```

Y luego:

```sql
SELECT * FROM messages ORDER BY id DESC LIMIT 10;
```

---

## 🛡️ Manejo de errores

- **Puerto ocupado** → El servidor muestra un error y finaliza.
- **Base de datos inaccesible** → Se interrumpe la ejecución con mensaje de error.
- **Errores al guardar mensaje** → Se registran en consola, pero el servidor sigue activo.

---

## ✒️ Autor

**Realizado por:** Fernando G. Espindola O.
