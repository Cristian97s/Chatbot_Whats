import customtkinter as ctk
from tkinter import messagebox
from threading import Thread
from Chatbot_Whats_POO import Conversacion, Contacto  # importa tus clases


class WhatsAppGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana principal
        self.title("🤖 WhatsApp Bot - Multi Sesiones")
        self.geometry("600x670")
        ctk.set_appearance_mode("dark")  # "light", "dark", "system"
        ctk.set_default_color_theme("green")  # "blue", "green", "dark-blue"

        # Variables
        self.num_bots = ctk.IntVar(value=1)
        self.num_contactos = ctk.IntVar(value=1)
        self.total_mensajes = ctk.IntVar(value=5)
        self.duracion_minutos = ctk.IntVar(value=5)

        self.conversacion = None  # se guarda aquí el objeto activo

        # Frame principal
        frame = ctk.CTkFrame(self, corner_radius=15)
        frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Widgets de entrada
        ctk.CTkLabel(frame, text="Número de navegadores (sesiones):").pack(pady=5)
        ctk.CTkEntry(frame, textvariable=self.num_bots, width=200).pack()

        ctk.CTkLabel(frame, text="Cantidad de contactos:").pack(pady=5)
        ctk.CTkEntry(frame, textvariable=self.num_contactos, width=200).pack()

        ctk.CTkLabel(frame, text="Nombres de los contactos (uno por línea):").pack(pady=5)
        self.contactos_entry = ctk.CTkTextbox(frame, height=100, width=400)
        self.contactos_entry.insert("1.0", "Juniet\nBisk\nCrist\nBot")
        self.contactos_entry.pack(pady=5)

        ctk.CTkLabel(frame, text="Cantidad total de mensajes:").pack(pady=5)
        ctk.CTkEntry(frame, textvariable=self.total_mensajes, width=200).pack()

        ctk.CTkLabel(frame, text="Duración de la conversación (minutos):").pack(pady=5)
        ctk.CTkEntry(frame, textvariable=self.duracion_minutos, width=200).pack()

        # Botones de control
        ctk.CTkButton(frame, text="🚀 Iniciar Conversación", command=self.start_conversacion).pack(pady=10)
        ctk.CTkButton(frame, text="🛑 Cerrar Navegadores", fg_color="red", hover_color="darkred", command=self.cerrar_navegadores).pack(pady=10)
        ctk.CTkButton(frame, text="❌ Salir", fg_color="gray", hover_color="black", command=self.quit).pack(pady=10)

        # Área de logs
        ctk.CTkLabel(frame, text="Logs:").pack(pady=5)
        self.log_area = ctk.CTkTextbox(frame, height=180, width=500)
        self.log_area.pack(pady=5)

    def log(self, msg):
        self.log_area.insert("end", msg + "\n")
        self.log_area.see("end")

    def start_conversacion(self):
        try:
            num_bots = self.num_bots.get()
            num_contactos = self.num_contactos.get()
            contactos_text = self.contactos_entry.get("1.0", "end").strip().split("\n")
            contactos = [Contacto(nombre.strip()) for nombre in contactos_text if nombre.strip()]

            if len(contactos) != num_contactos:
                messagebox.showerror("Error", "El número de contactos no coincide con lo escrito.")
                return

            total_mensajes = self.total_mensajes.get()
            duracion_minutos = self.duracion_minutos.get()

            def run_bot():
                self.conversacion = Conversacion(num_bots, contactos, total_mensajes, duracion_minutos)
                self.log("🚀 Iniciando conversación...")
                self.conversacion.iniciar()
                self.log("✅ Conversación terminada. Esperando orden de cierre...")

            Thread(target=run_bot, daemon=True).start()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def cerrar_navegadores(self):
        if self.conversacion:
            self.conversacion.cerrar_todos()
            self.log("🛑 Todos los navegadores cerrados por el usuario.")
            self.conversacion = None
        else:
            messagebox.showinfo("Info", "No hay navegadores activos para cerrar.")


if __name__ == "__main__":
    app = WhatsAppGUI()
    app.mainloop()
