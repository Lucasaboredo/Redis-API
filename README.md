# 🌌 Práctica #2 - Alquiler de Capítulos de The Mandalorian (Redis)

## 📝 Descripción
Esta aplicación web full-stack fue desarrollada con **Flask** (Backend en Python) y **Vanilla JS/CSS** (Frontend) para interactuar directamente con una base de datos **Redis**. 

El objetivo principal es gestionar el estado de alquiler de la lista oficial de capítulos de las 3 temporadas de *The Mandalorian*. Todo el estado de disponibilidad se maneja en tiempo real mediante el uso de almacenamiento de llaves (strings) y tiempos de expiración (TTL) en Redis.

### Lógica de Estados:
- **🟢 Disponible:** El capítulo no cuenta con una key activa en Redis.
- **🟡 Reservado:** Al solicitar alquilar el capítulo, se crea la key `mando:ep:S01E01` (ejemplo) con el valor `Reservado` y un TTL de **4 minutos** (240 segundos). Si no se paga, la key se destruye automáticamente y vuelve a estar "Disponible".
- **🟩 Alquilado:** Si se confirma el pago mientras está reservado, el valor cambia a `Alquilado` y el TTL de la key se extiende a **24 horas** (86400 segundos).

---

## 🚀 ¿Cómo arrancarlo?

### 1. Iniciar Redis (con Docker)
Si tienes el motor de Docker instalado, levanta un contenedor de Redis en el puerto por defecto (6379):
```bash
docker run --name mi_redis -p 6379:6379 -d redis
```

### 2. Instalar las dependencias de Python
Abre una terminal en la carpeta del proyecto y ejecuta:
```bash
pip install flask redis
```

### 3. Ejecutar el Servidor
Inicia la aplicación de Flask ejecutando:
```bash
python app.py
```
El servidor se levantará en [http://localhost:5000](http://localhost:5000) donde podrás ver e interactuar con la interfaz gráfica oficial.

---

## 🐳 ¿Cómo probarlo por detrás usando Docker y redis-cli?

El profesor seguramente quiera validar que los datos se están guardando en Redis correctamente. Para probarlo mediante la consola, sigue estos pasos:

### 1. Entrar al CLI de tu contenedor Redis
Con el contenedor de Redis encendido (`mi_redis`), abre una terminal y ejecuta:
```bash
docker exec -it mi_redis redis-cli
```

### 2. Monitorear los Cambios (Comandos Útiles)
Una vez adentro del `redis-cli`, puedes jugar con la interfaz visual en tu navegador y luego ejecutar estos comandos en la consola para demostrar que todo funciona:

* **Ver todas las llaves (capítulos que fueron tocados):**
  ```bash
  keys mando:ep:*
  ```

* **Revisar el estado actual de un capítulo en particular (ej. Capítulo 1 de la Temporada 1):**
  ```bash
  get mando:ep:S01E01
  ```
  *(Devolverá "Reservado" o "Alquilado". Si devuelve (nil), el capítulo está Disponible).*

* **Ver cuánto tiempo le queda a la reserva (TTL):**
  ```bash
  ttl mando:ep:S01E01
  ```
  *(Si acabas de reservarlo en la Web, verás un contador en segundos bajando desde 240. Si ya lo pagaste, bajará desde 86400).*

### 3. Simular Acciones directo desde Consola (Sin la Web)
También puedes simular el comportamiento desde el `redis-cli` como lo haría la Web:

* **Reservar un capítulo a mano por 4 minutos (240 seg):**
  ```bash
  set mando:ep:S02E03 "Reservado" ex 240 nx
  ```

* **Confirmar su pago (extenderlo a 24 horas):**
  ```bash
  set mando:ep:S02E03 "Alquilado" ex 86400
  ```
