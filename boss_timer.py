
import tkinter as tk
from PIL import Image, ImageTk
import time
import pygame
from datetime import datetime, timedelta
import keyboard
import pyperclip

# Funções de som
def play_sound(sound_path):
    if sound_enabled.get():
        pygame.mixer.init()
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play()

def toggle_sound():
    current_state = sound_enabled.get()
    sound_enabled.set(not current_state)
    update_sound_menu()

def update_sound_menu():
    if sound_enabled.get():
        config_menu.entryconfig(0, label="Desativar Som")
    else:
        config_menu.entryconfig(0, label="Ativar Som")

# Classe BossTimer
class BossTimer:
    def __init__(self, root, image_path, sound_path, label_text, row, column, section):
        self.image_path = image_path
        self.sound_path = sound_path
        self.label_text = label_text
        self.end_time = 0
        self.section = section

        self.frame = tk.Frame(root, bg="#333333", padx=5, pady=5, borderwidth=1, relief="solid")
        self.frame.grid(row=row, column=column, padx=5, pady=5, sticky='nsew')

        self.load_image()
        self.create_widgets()

        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=3)
        self.frame.grid_columnconfigure(2, weight=2)
        self.frame.grid_columnconfigure(3, weight=1)
        
    def load_image(self):
        try:
            self.boss_image = Image.open(self.image_path).resize((40, 40))
            self.boss_image = ImageTk.PhotoImage(self.boss_image)
        except FileNotFoundError:
            print(f"Erro: Arquivo de imagem não encontrado - {self.image_path}")
            self.boss_image = ImageTk.PhotoImage(Image.new('RGB', (40, 40), color='gray'))
        
        self.label_image = tk.Label(self.frame, image=self.boss_image, bg="#333333")
        self.label_image.grid(row=0, column=0, padx=5, pady=5, sticky='w')

    def create_widgets(self):
        self.timer_label = tk.Label(self.frame, text=self.label_text, font=("Helvetica", 10), fg="#ffffff", bg="#333333")
        self.timer_label.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        self.time_label = tk.Label(self.frame, text="", font=("Helvetica", 8), fg="#cccccc", bg="#333333")
        self.time_label.grid(row=0, column=2, padx=5, pady=5, sticky='w')

        self.checkbox_var = tk.IntVar()
        self.checkbox = tk.Checkbutton(
            self.frame, 
            text="Iniciar", 
            variable=self.checkbox_var, 
            command=self.start_timer, 
            bg="#333333", 
            fg="#ffffff", 
            selectcolor="#555555",
            font=("Helvetica", 8)
        )
        self.checkbox.grid(row=0, column=3, padx=5, pady=5, sticky='w')

    def play_sound(self):
        play_sound(self.sound_path)
    
    def start_timer(self):
        if self.checkbox_var.get():
            self.end_time = time.time() + 15 * 60
            self.update_timer()
    
    def update_timer(self):
        if self.checkbox_var.get():
            if time.time() >= self.end_time:
                self.play_sound()
                self.checkbox_var.set(0)
                self.time_label.config(text="")
            else:
                remaining = int(self.end_time - time.time())
                minutes, seconds = divmod(remaining, 60)
                self.timer_label.config(text=f"Tempo restante: {minutes:02}:{seconds:02}")

                appearance_time = datetime.now() + timedelta(seconds=remaining)
                appearance_str = appearance_time.strftime("%H:%M:%S")
                self.time_label.config(text=f"Reaparecerá às: {appearance_str}")

                root.after(1000, self.update_timer)
        else:
            self.timer_label.config(text=self.label_text)
            self.time_label.config(text="")

# Funções de interação
def toggle_checkbox(boss_index):
    boss_timers[boss_index].checkbox_var.set(1 - boss_timers[boss_index].checkbox_var.get())
    boss_timers[boss_index].start_timer()

def update_hotkeys():
    global hotkeys
    for hotkey in hotkeys:
        if hotkey in keyboard._hotkeys:
            keyboard.remove_hotkey(hotkey)
    
    for i, hotkey in enumerate(hotkeys):
        if hotkey:
            try:
                keyboard.add_hotkey(hotkey, lambda i=i: toggle_checkbox(i))
            except ValueError as e:
                print(f"Erro ao adicionar hotkey {hotkey}: {e}")

def copy_to_clipboard(text):
    pyperclip.copy(text)

def on_label_click(event):
    copy_to_clipboard("0xE6d8012003485bAB10Cfe9B13Db2354e358C8F4a")

def on_label_hover(event):
    label_copy.config(cursor="hand2")

def show_tooltip(event):
    global tooltip
    if tooltip is not None:
        return
    
    tooltip = tk.Toplevel(root)
    tooltip.wm_overrideredirect(True)
    tooltip.wm_geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
    label = tk.Label(tooltip, text="Copiar", background="lightyellow", relief="solid", borderwidth=1)
    label.pack()
    root.after(2000, hide_tooltip)

def hide_tooltip():
    global tooltip
    if tooltip is not None:
        tooltip.destroy()
        tooltip = None

# Configuração da interface
root = tk.Tk()
root.title("Metacene Boss Timer 0.1")
root.configure(bg="#1e1e1e")

# Remove o ícone da janela
try:
    icon_image = Image.open("C:/Users/new/Downloads/meta.png")
    icon_photo = ImageTk.PhotoImage(icon_image)
    root.iconphoto(True, icon_photo)
except Exception as e:
    print(f"Erro ao carregar ícone: {e}")

sound_enabled = tk.BooleanVar(value=True)

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

config_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Configurações", menu=config_menu)
config_menu.add_command(label="Desativar Som", command=toggle_sound)

update_sound_menu()

tk.Label(root, text="Rotação de Cima", font=("Helvetica", 12, "bold"), fg="#ffffff", bg="#1e1e1e").grid(row=0, column=0, columnspan=4, pady=10)
tk.Label(root, text="Rotação de Baixo", font=("Helvetica", 12, "bold"), fg="#ffffff", bg="#1e1e1e").grid(row=6, column=0, columnspan=4, pady=10)
tk.Label(root, text="Rotação da Direita", font=("Helvetica", 12, "bold"), fg="#ffffff", bg="#1e1e1e").grid(row=12, column=0, columnspan=4, pady=10)


discord_label = tk.Label(root, text="Discord: @newnft0", font=("Helvetica", 10), fg="#ffffff", bg="#1e1e1e")
discord_label.grid(row=0, column=0, padx=10, pady=10, sticky='nw')


boss_timers = [
    # Rotação de Cima
    BossTimer(root, "C:/Users/new/Documents/python/adriano.png", "C:/Users/new/Documents/python/sound.mp3", "Adv cris spirit", 1, 0, "cima"),
    BossTimer(root, "C:/Users/new/Documents/python/cesafilho.png", "C:/Users/new/Documents/python/sound.mp3", "Ironclad monkey", 1, 1, "cima"),
    BossTimer(root, "C:/Users/new/Documents/python/cristiano.png", "C:/Users/new/Documents/python/sound.mp3", "Cris spirit", 2, 0, "cima"),
    BossTimer(root, "C:/Users/new/Documents/python/serpent.png", "C:/Users/new/Documents/python/sound.mp3", "Green-winged serpent", 2, 1, "cima"),
    BossTimer(root, "C:/Users/new/Documents/python/robo.png", "C:/Users/new/Documents/python/sound.mp3", "Mechanoid", 3, 0, "cima"),
    BossTimer(root, "C:/Users/new/Documents/python/peixeilha.png", "C:/Users/new/Documents/python/sound.mp3", "Scourge Mid", 3, 1, "cima"),

    # Rotação de Baixo
    BossTimer(root, "C:/Users/new/Documents/python/polvoverde.png", "C:/Users/new/Documents/python/sound.mp3", "Octopus up", 8, 0, "cima"),
    BossTimer(root, "C:/Users/new/Documents/python/polvobaixo.png", "C:/Users/new/Documents/python/sound.mp3", "Octopus down", 8, 1, "baixo"),
    BossTimer(root, "C:/Users/new/Documents/python/peixebaixo.png", "C:/Users/new/Documents/python/sound.mp3", "scourge down", 9, 0, "baixo"),

    # Rotação de Direita
    BossTimer(root, "C:/Users/new/Documents/python/treant.png", "C:/Users/new/Documents/python/sound.mp3", "BlazeTreant", 13, 0, "direita"),
    BossTimer(root, "C:/Users/new/Documents/python/bat.png", "C:/Users/new/Documents/python/sound.mp3", "Red ear bat", 13, 1, "direita"),
    BossTimer(root, "C:/Users/new/Documents/python/peixedireita.png", "C:/Users/new/Documents/python/sound.mp3", "Scourge up", 14, 0, "direita"),
]

hotkeys = [
    'ctrl+1', 'ctrl+2', 'ctrl+3', 'ctrl+4', 'ctrl+5', 'ctrl+6',  # Rotação de Cima
    'alt+1', 'alt+2', 'alt+3',  # Rotação de Baixo
    'alt+4', 'alt+5', 'alt+6'   # Rotação de Direita
]
update_hotkeys()

tooltip = None

label_copy = tk.Label(root, text="apoie com mud: 0xE6d8012003485bAB10Cfe9B13Db2354e358C8F4a", fg="white", cursor="hand2", bg="#1e1e1e")
label_copy.grid(row=15, column=0, columnspan=2)
label_copy.bind("<Button-1>", on_label_click)
label_copy.bind("<Enter>", on_label_hover)
label_copy.bind("<Motion>", show_tooltip)

root.mainloop()
