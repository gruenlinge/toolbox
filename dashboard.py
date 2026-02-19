import tkinter as tk 
from tkinter import scrolledtext 
import sys 
from pathlib import Path 
 
# Damit der Importer die Module im SYSTEM-Ordner findet 
SYSTEM_DIR = Path(__file__).parent / "SYSTEM" 
sys.path.insert(0, str(SYSTEM_DIR)) 
 
from file_manager import FilePaths 
from logger import Logger 
 
log = Logger() 
 
class Dashboard: 
    def __init__(self, root): 
        self.root = root 
        self.root.title("Projekt-Dashboard (Hauptverzeichnis)") 
        self.root.geometry("600x500") 
 
        tk.Label(root, text="Willkommen im Dashboard", font=("Arial", 16)).pack(pady=10) 
 
        pfad_frame = tk.LabelFrame(root, text="Projekt-Pfade", padx=10, pady=5) 
        pfad_frame.pack(fill="x", padx=10, pady=5) 
 
        pfade = [ 
            ("Basis:", FilePaths.BASE_DIR), 
            ("SYSTEM:", FilePaths.SYSTEM_DIR), 
            ("Konfiguration:", FilePaths.CONFIG_DIR), 
            ("Eingabe:", FilePaths.INPUT_DIR), 
            ("Ausgabe:", FilePaths.OUTPUT_DIR), 
        ] 
        for label, path in pfade: 
            tk.Label(pfad_frame, text=f"{label} {path}", font=("Courier", 8), anchor="w").pack(fill="x") 
 
        log_frame = tk.LabelFrame(root, text="Log-Ausgaben", padx=10, pady=5) 
        log_frame.pack(fill="both", expand=True, padx=10, pady=5) 
 
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, font=("Courier", 9)) 
        self.log_text.pack(fill="both", expand=True) 
 
        btn_frame = tk.Frame(root) 
        btn_frame.pack(pady=10) 
 
        tk.Button(btn_frame, text="Info loggen", command=self.log_info).pack(side="left", padx=5) 
        tk.Button(btn_frame, text="Warnung loggen", command=self.log_warning).pack(side="left", padx=5) 
        tk.Button(btn_frame, text="Fehler loggen", command=self.log_error).pack(side="left", padx=5) 
        tk.Button(btn_frame, text="Beenden", command=root.quit).pack(side="left", padx=20) 
 
        log.info("Dashboard gestartet") 
        self.log_message("INFO", "Dashboard gestartet") 
 
    def log_info(self): 
        log.info("Info-Button gedr…kt") 
        self.log_message("INFO", "Info-Button gedr…kt") 
 
    def log_warning(self): 
        log.warning("Warnung-Button gedr…kt") 
        self.log_message("WARNUNG", "Warnung-Button gedr…kt") 
 
    def log_error(self): 
        log.error("Fehler-Button gedr…kt") 
        self.log_message("FEHLER", "Fehler-Button gedr…kt") 
 
    def log_message(self, level, text): 
        self.log_text.insert(tk.END, f"{level}: {text}\n") 
        self.log_text.see(tk.END) 
 
if __name__ == "__main__": 
    root = tk.Tk() 
    app = Dashboard(root) 
    root.mainloop() 
