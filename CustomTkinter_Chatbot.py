import customtkinter as ctk
from tkinter import messagebox
from threading import Thread
from Chatbot_Whats_POO import Conversacion, Contacto

class WhatsAppGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("🤖 WhatsApp Bot - Multi Sesiones")
        self.geometry("750x700")
        self.minsize(700, 650)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        # Variables
        self.num_bots = ctk.IntVar(value=1)
        self.total_mensajes = ctk.IntVar(value=5)
        self.duracion_minutos = ctk.IntVar(value=5)
        self.conversacion = None

        self.contactos_blocks = []  # aquí guardamos cada bloque de contactos por sesión

        # ====== FRAME CONFIGURACIÓN GENERAL ======
        frame_config = ctk.CTkFrame(self, corner_radius=15)
        frame_config.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(frame_config, text="⚙️ Configuración General", font=("Arial", 16, "bold")).pack(pady=10)

        grid = ctk.CTkFrame(frame_config)
        grid.pack(pady=5)

        ctk.CTkLabel(grid, text="Número de Navegadores (sesiones):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        num_bots_entry = ctk.CTkEntry(grid, textvariable=self.num_bots, width=120)
        num_bots_entry.grid(row=0, column=1, padx=5, pady=5)

        ctk.CTkLabel(grid, text="Cantidad total de mensajes:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        ctk.CTkEntry(grid, textvariable=self.total_mensajes, width=120).grid(row=0, column=3, padx=5, pady=5)

        ctk.CTkLabel(grid, text="Duración (minutos):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        ctk.CTkEntry(grid, textvariable=self.duracion_minutos, width=120).grid(row=1, column=1, padx=5, pady=5)

        ctk.CTkButton(grid, text="Actualizar Bloques de Contactos", command=self.crear_bloques_contactos).grid(row=1, column=2, columnspan=2, padx=5, pady=5)

        # ====== FRAME SCROLLABLE PARA BLOQUES DE CONTACTOS ======
        scroll_frame = ctk.CTkScrollableFrame(self, corner_radius=15)
        scroll_frame.pack(pady=10, padx=20, fill="both", expand=True)
        self.scroll_frame = scroll_frame

        # ====== FRAME ACCIONES ======
        frame_acciones = ctk.CTkFrame(self, corner_radius=15)
        frame_acciones.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(frame_acciones, text="🎮 Controles", font=("Arial", 16, "bold")).pack(pady=10)

        btn_frame = ctk.CTkFrame(frame_acciones, fg_color="transparent")
        btn_frame.pack(pady=5)

        ctk.CTkButton(btn_frame, text="🚀 Iniciar Conversación", width=220, height=40,
                      command=self.start_conversacion).grid(row=0, column=0, padx=10, pady=5)

        ctk.CTkButton(btn_frame, text="🛑 Cerrar Navegadores", width=220, height=40,
                      fg_color="red", hover_color="darkred", command=self.cerrar_navegadores).grid(row=0, column=1, padx=10, pady=5)

        # ====== FRAME LOGS ======
        frame_logs = ctk.CTkFrame(self, corner_radius=15)
        frame_logs.pack(pady=10, padx=20, fill="both", expand=True)

        ctk.CTkLabel(frame_logs, text="📜 Logs de Ejecución", font=("Arial", 16, "bold")).pack(pady=10)

        self.log_area = ctk.CTkTextbox(frame_logs, height=200, width=700, corner_radius=10)
        self.log_area.pack(pady=5, padx=10, fill="both", expand=True)

    # ==== Métodos ====
    def log(self, msg):
        self.log_area.insert("end", msg + "\n")
        self.log_area.see("end")

    def crear_bloques_contactos(self):
        # limpiar bloques viejos
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        self.contactos_blocks = []

        num_bots = self.num_bots.get()
        for i in range(num_bots):
            frame = ctk.CTkFrame(self.scroll_frame, corner_radius=10)
            frame.pack(pady=8, padx=10, fill="x")

            ctk.CTkLabel(frame, text=f"🧑 Contactos Bot {i+1}", font=("Arial", 14, "bold")).pack(pady=5)
            ctk.CTkLabel(frame, text="Número de contactos:").pack(pady=2)
            num_contactos_var = ctk.IntVar(value=1)
            ctk.CTkEntry(frame, textvariable=num_contactos_var, width=100).pack(pady=2)

            ctk.CTkLabel(frame, text="Nombres de contactos (uno por línea):").pack(pady=2)
            textbox = ctk.CTkTextbox(frame, height=80, width=500)
            textbox.insert("1.0", f"Contacto_{i+1}_1\nContacto_{i+1}_2")
            textbox.pack(pady=5)

            self.contactos_blocks.append({
                "num_contactos": num_contactos_var,
                "textbox": textbox
            })

    def start_conversacion(self):
        try:
            bots_contactos = []
            for block in self.contactos_blocks:
                contactos_text = block["textbox"].get("1.0", "end").strip().split("\n")
                contactos = [Contacto(nombre.strip()) for nombre in contactos_text if nombre.strip()]
                if len(contactos) != block["num_contactos"].get():
                    messagebox.showerror("Error", "Número de contactos no coincide con los escritos.")
                    return
                bots_contactos.append(contactos)

            total_mensajes = self.total_mensajes.get()
            duracion_minutos = self.duracion_minutos.get()
            num_bots = self.num_bots.get()

            def run_bot():
                # Aquí se asume que la clase Conversacion puede aceptar listas de contactos por bot
                self.conversacion = Conversacion(num_bots=len(bots_contactos), total_mensajes=total_mensajes, duracion_minutos=duracion_minutos, bots_contactos=bots_contactos)
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
