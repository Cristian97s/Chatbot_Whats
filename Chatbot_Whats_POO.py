from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from translate import Translator
import time
import requests
import random

class Contacto:
    def __init__(self, nombre):
        self.nombre = nombre

class WhatsAppBot:
    def __init__(self, contactos, session_id):
        self.contactos = contactos  # lista de objetos Contacto
        self.session_id = session_id
        self.driver = webdriver.Chrome()
        self.driver.get("https://web.whatsapp.com")
        print(f"🟢 Escanea el código QR en el navegador {self.session_id}")
        WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
        )

    def enviar_mensaje(self, contacto, mensaje, limite=500):
        # Buscar contacto
        search_box = self.driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
        search_box.click()
        search_box.clear()
        search_box.send_keys(contacto.nombre)
        search_box.send_keys(Keys.ENTER)
        time.sleep(1)

        # Caja de mensaje
        message_box = self.driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
        message_box.click()

        # Dividir mensaje largo en partes
        mensajes = [mensaje[i:i+limite] for i in range(0, len(mensaje), limite)]
        actions = ActionChains(self.driver)

        for msg in mensajes:
            actions.move_to_element(message_box).click()
            for letra in msg:
                actions.send_keys(letra)
                time.sleep(random.uniform(0.01, 0.05))  # simula tipeo humano
            actions.send_keys(Keys.ENTER)
        actions.perform()
        print(f"✅ Mensaje enviado a {contacto.nombre} en sesión {self.session_id}")

    def cerrar(self):
        self.driver.quit()

class QuoteTranslator:
    def __init__(self, from_lang="en", to_lang="es"):
        self.translator = Translator(from_lang=from_lang, to_lang=to_lang)

    def obtener_cita_traducida(self):
        url = "https://thequoteshub.com/api/"
        response = requests.get(url)
        data = response.json()
        texto = f"{data['text']} Autor: {data['author']}"
        partes = [texto[i:i+480] for i in range(0, len(texto), 480)]
        traducciones = [self.translator.translate(parte) for parte in partes]
        return " ".join(traducciones)

class Conversacion:
    def __init__(self, num_bots, contactos, total_mensajes, duracion_minutos, min_delay=5, max_delay=15):
        self.total_mensajes = total_mensajes
        self.duracion_total = duracion_minutos * 60
        self.min_delay = min_delay
        self.max_delay = max_delay

        # Repartimos contactos entre los bots
        contactos_por_bot = [[] for _ in range(num_bots)]
        for i, c in enumerate(contactos):
            contactos_por_bot[i % num_bots].append(c)

        self.bots = [WhatsAppBot(contactos_por_bot[i], i+1) for i in range(num_bots)]
        self.mensajes_por_bot = self._repartir_mensajes(num_bots)

    def _repartir_mensajes(self, num_bots):
        mensajes = [0] * num_bots
        for _ in range(self.total_mensajes):
            idx = random.randint(0, num_bots - 1)
            mensajes[idx] += 1
        print("📊 Distribución de mensajes por bot:", mensajes)
        return mensajes

    def iniciar(self):
        quote_translator = QuoteTranslator()
        start_time = time.time()
        end_time = start_time + self.duracion_total

        last_bot_idx = None
        consecutive_count = 0
        max_consecutive = 2

        while time.time() < end_time:
            pendientes = [i for i, m in enumerate(self.mensajes_por_bot) if m > 0]
            if not pendientes:
                break

            posibles = [i for i in pendientes if i != last_bot_idx or consecutive_count < max_consecutive]
            if not posibles:
                posibles = pendientes

            bot_idx = random.choice(posibles)
            bot = self.bots[bot_idx]

            contacto = random.choice(bot.contactos)
            mensaje = quote_translator.obtener_cita_traducida()
            bot.enviar_mensaje(contacto, mensaje)
            self.mensajes_por_bot[bot_idx] -= 1

            if bot_idx == last_bot_idx:
                consecutive_count += 1
            else:
                last_bot_idx = bot_idx
                consecutive_count = 1

            # Espera aleatoria simulando conversación
            delay = random.uniform(self.min_delay, self.max_delay)
            time.sleep(delay)

    def cerrar_todos(self):
        for bot in self.bots:
            bot.cerrar()

if __name__ == "__main__":
    # num_bots = int(input("¿Cuántos navegadores (sesiones de WhatsApp) quieres abrir?: "))
    # num_contactos = int(input("Cantidad de contactos: "))
    # contactos = [Contacto(input(f"Nombre del contacto {i+1}: ")) for i in range(num_contactos)]
    # total_mensajes = int(input("Cantidad total de mensajes a enviar: "))
    # duracion_minutos = int(input("Duración total de la conversación (en minutos): "))
    
    #conversacion = Conversacion(num_bots, contactos, total_mensajes, duracion_minutos, min_delay=5, max_delay=12)
    #conversacion.iniciar()

    # input("Presiona Enter para cerrar todos los navegadores...")
    # conversacion.cerrar_todos()
    
    # Solo arrancar la GUI
    from CustomTkinter_Chatbot import WhatsAppGUI  # importa tu clase GUI
    app = WhatsAppGUI()
    app.mainloop()