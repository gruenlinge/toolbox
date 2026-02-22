#!/usr/bin/env python
# coding: utf-8
"""
dashboard.py ? Minimales Dashboard fur das Projekt.
Steht im Hauptverzeichnis, importiert Module aus dem SYSTEM-Ordner.
Erweiterung: Kann Skripte aus dem SYSTEM-Ordner starten und Ausgabe anzeigen.
"""

import tkinter as tk
from tkinter import scrolledtext
import sys
import subprocess
import threading
import queue
from pathlib import Path

# Damit der Importer die Module im SYSTEM-Ordner findet
SYSTEM_DIR = Path(__file__).parent / "SYSTEM"
sys.path.insert(0, str(SYSTEM_DIR))

# Jetzt konnen die Module importiert werden
from file_manager import FilePaths
from logger import Logger

# Logger initialisieren
log = Logger()

class Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Projekt-Dashboard (Hauptverzeichnis)")
        self.root.geometry("700x600")

        # Queue fur Thread-sichere Kommunikation
        self.msg_queue = queue.Queue()

        # Uberschrift
        tk.Label(root, text="Willkommen im Dashboard", font=("Arial", 16)).pack(pady=10)

        # Pfad-Anzeige
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

        # Log-Fenster
        log_frame = tk.LabelFrame(root, text="Log-Ausgaben", padx=10, pady=5)
        log_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, font=("Courier", 9))
        self.log_text.pack(fill="both", expand=True)

        # Button-Frame
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Info loggen", command=self.log_info).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Warnung loggen", command=self.log_warning).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Fehler loggen", command=self.log_error).pack(side="left", padx=5)

        # NEU: Button zum Starten eines Test-Skripts
        tk.Button(btn_frame, text="Test-Skript starten", command=self.run_test_script).pack(side="left", padx=5)

        tk.Button(btn_frame, text="Beenden", command=root.quit).pack(side="left", padx=20)

        # Erste Log-Meldung
        log.info("Dashboard gestartet")
        self.log_message("INFO", "Dashboard gestartet")

        # Queue regelmasig abfragen
        self.root.after(100, self.process_queue)

    def log_info(self):
        log.info("Info-Button gedruckt")
        self.log_message("INFO", "Info-Button gedruckt")

    def log_warning(self):
        log.warning("Warnung-Button gedruckt")
        self.log_message("WARNUNG", "Warnung-Button gedruckt")

    def log_error(self):
        log.error("Fehler-Button gedruckt")
        self.log_message("FEHLER", "Fehler-Button gedruckt")

    def log_message(self, level, text):
        """Zeigt eine Meldung im Log-Fenster an."""
        self.log_text.insert(tk.END, f"{level}: {text}\n")
        self.log_text.see(tk.END)

    # NEU: Methode zum Starten des Test-Skripts
    def run_test_script(self):
        """Startet test_logger.py in einem separaten Thread und zeigt Ausgabe an."""
        script_path = SYSTEM_DIR / "test_logger.py"
        if not script_path.exists():
            self.log_message("FEHLER", f"Skript nicht gefunden: {script_path}")
            return

        self.log_message("INFO", f"Starte {script_path.name} ...")
        # Thread starten, um GUI nicht zu blockieren
        thread = threading.Thread(target=self._run_script_thread, args=(script_path,), daemon=True)
        thread.start()

    def _run_script_thread(self, script_path):
        """Fuhrt das Skript aus und leitet Ausgabe in die Queue."""
        try:
            # Verwende denselben Python-Interpreter wie das Dashboard
            python_exe = sys.executable
            process = subprocess.Popen(
                [python_exe, str(script_path)],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                encoding='utf-8'
            )
            # Zeilenweise lesen und in Queue packen
            for line in iter(process.stdout.readline, ''):
                if line:
                    self.msg_queue.put(("STDOUT", line.rstrip()))
            process.wait()
            if process.returncode == 0:
                self.msg_queue.put(("INFO", f"{script_path.name} erfolgreich beendet."))
            else:
                self.msg_queue.put(("FEHLER", f"{script_path.name} mit Fehler {process.returncode} beendet."))
        except Exception as e:
            self.msg_queue.put(("FEHLER", f"Fehler beim Ausfuhren: {e}"))

    def process_queue(self):
        """Verarbeitet Nachrichten aus der Queue (wird regelmasig von Tkinter aufgerufen)."""
        try:
            while True:
                msg_type, msg = self.msg_queue.get_nowait()
                if msg_type == "STDOUT":
                    self.log_message("", msg)  # ohne Level
                elif msg_type == "INFO":
                    self.log_message("INFO", msg)
                elif msg_type == "FEHLER":
                    self.log_message("FEHLER", msg)
                else:
                    self.log_message("", msg)
        except queue.Empty:
            pass
        self.root.after(100, self.process_queue)

if __name__ == "__main__":
    root = tk.Tk()
    app = Dashboard(root)
    root.mainloop()