# Chatbot_Whats

Este proyecto es un **bot de WhatsApp** que envía mensajes automáticos a múltiples contactos, con simulación de conversación humana y traducción de citas al español. Está implementado en **Python** utilizando **Selenium**.

---

## ⚡ Características

- Enviar mensajes a múltiples contactos de WhatsApp Web.
- Traducción automática de citas del inglés al español.
- Simulación de tipeo humano letra por letra.
- Retrasos aleatorios entre mensajes para simular conversación real.
- Evita enviar demasiados mensajes seguidos al mismo contacto.
- Modular y fácil de mantener gracias a la programación orientada a objetos.

---

## 🛠 Requisitos

- Python 3.10 o superior.
- Google Chrome instalado.
- ChromeDriver compatible con tu versión de Chrome.
- Librerías de Python necesarias (puedes instalarlas con `pip`):

```bash
pip install selenium requests translate
```

Nota: Asegúrate de que chromedriver esté en tu PATH o en la misma carpeta que el script.

---

### 🚀 Instalación

1. Clona este repositorio:

```bash
git clone https://github.com/Cristian97s/Chatbot_Whats.git
cd Chatbot_Whats
```
2. Crea el entorno virtual:
```bash
cd Chatbot_Whats
venv\Scripts\activate   # en Windows
```
3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

### 💽 Crear un Ejecutable

1. Haber instalado las dependencias
```bash
pip install -r requirements.txt
pip install pyinstaller
pyinstaller --onefile --windowed --icon=bot.ico Chatbot_Whats_POO.py --name "Chatbot_Whats"
```

### 👉 El .exe resultante quedará en la carpeta:
```bash
Chatbot_Whats/dist/Chatbot_Whats.exe
```
---

### 📝 Uso

Ejecuta el script principal:

```bash
python CustomTkinter_Chatbot.py
```

---

### 🧩 Estructura del proyecto

```bash
Chatbot_Whats/
├─ Chatbot_Whats_POO.py    # Script principal
├─ CustomTkinter_Chatbot   # Interfaz grafica
├─ README.md               # Documentación
└─ requirements.txt        # Requerimientos
```

---

### ⚠ Advertencias

- Este bot interactúa con WhatsApp Web, por lo que tu cuenta puede estar sujeta a bloqueos si se detecta actividad sospechosa.

- Se recomienda usarlo con precaución y solo con fines educativos.

- Evita enviar mensajes masivos a personas que no deseen recibirlos.