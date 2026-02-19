# SYSTEM/logger.py
"""Einfacher Logger für Konsolen- und Dateiausgabe."""

import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, TextIO

# Log-Level
LEVELS = {
    "DEBUG": 10,
    "INFO": 20,
    "WARNING": 30,
    "ERROR": 40,
    "CRITICAL": 50,
}

class Logger:
    """Logger mit Ausgabe in Datei und optional auf Konsole."""

    def __init__(self, log_file: Optional[Path] = None, console: bool = True, min_level: str = "INFO"):
        """
        Args:
            log_file: Pfad zur Logdatei (wenn None, wird nur auf Konsole geschrieben)
            console: Ausgabe auf Konsole aktivieren?
            min_level: Minimales Level (z.B. "INFO" – DEBUG wird dann ignoriert)
        """
        self.log_file = Path(log_file) if log_file else None
        self.console = console
        self.min_level = LEVELS.get(min_level.upper(), 20)

        # Falls Logdatei angegeben, Verzeichnis anlegen
        if self.log_file:
            self.log_file.parent.mkdir(parents=True, exist_ok=True)

    def _write(self, level: str, message: str):
        """Schreibt eine formatierte Nachricht in Datei und/oder Konsole."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        level_padded = level.ljust(8)
        formatted = f"{timestamp} | {level_padded} | {message}"

        # In Datei schreiben
        if self.log_file:
            try:
                with open(self.log_file, "a", encoding="utf-8") as f:
                    f.write(formatted + "\n")
            except Exception:
                # Falls Datei nicht beschreibbar, zumindest auf Konsole ausgeben (falls erlaubt)
                if self.console:
                    print(f"FEHLER: Konnte nicht in Logdatei schreiben: {self.log_file}", file=sys.stderr)

        # Auf Konsole ausgeben
        if self.console:
            if level in ("ERROR", "CRITICAL"):
                print(formatted, file=sys.stderr)
            else:
                print(formatted)

    def debug(self, message: str):
        if self.min_level <= LEVELS["DEBUG"]:
            self._write("DEBUG", message)

    def info(self, message: str):
        if self.min_level <= LEVELS["INFO"]:
            self._write("INFO", message)

    def warning(self, message: str):
        if self.min_level <= LEVELS["WARNING"]:
            self._write("WARNING", message)

    def error(self, message: str):
        if self.min_level <= LEVELS["ERROR"]:
            self._write("ERROR", message)

    def critical(self, message: str):
        if self.min_level <= LEVELS["CRITICAL"]:
            self._write("CRITICAL", message)


# Globale Standard-Instanz (für einfachen Import)
_default_logger = None

def get_logger(log_file: Optional[Path] = None, console: bool = True, min_level: str = "INFO") -> Logger:
    """Erzeugt oder holt eine Logger-Instanz (Singleton für Standard)."""
    global _default_logger
    if _default_logger is None:
        _default_logger = Logger(log_file, console, min_level)
    return _default_logger

# Komfort-Funktionen für den Standard-Logger
def debug(msg): get_logger().debug(msg)
def info(msg): get_logger().info(msg)
def warning(msg): get_logger().warning(msg)
def error(msg): get_logger().error(msg)
def critical(msg): get_logger().critical(msg)