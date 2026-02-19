# SYSTEM/file_manager.py
"""Zentrale Pfadverwaltung für das gesamte Projekt.

Stellt sicher, dass alle wichtigen Verzeichnisse existieren und
bietet eine einheitliche Schnittstelle für den Zugriff auf Pfade.
"""

from pathlib import Path

# --- Basis-Pfad: Das Hauptverzeichnis des Projekts ---
# Diese Datei liegt in .../toolbox/SYSTEM/file_manager.py
# Also ist das Projekt-Root zwei Ebenen höher: .../toolbox/
BASE_DIR = Path(__file__).resolve().parent.parent

# --- Zentrale Daten-Ordner ---
DATA_DIR = BASE_DIR / "DATEN"
CONFIG_DIR = DATA_DIR / "CONFIG"
INPUT_DIR = DATA_DIR / "INPUT"
OUTPUT_DIR = DATA_DIR / "OUTPUT"

# --- System-Ordner (für Skripte und Hilfsmodule) ---
SYSTEM_DIR = BASE_DIR / "SYSTEM"

# --- Ordner automatisch anlegen (falls sie nicht existieren) ---
for directory in [DATA_DIR, CONFIG_DIR, INPUT_DIR, OUTPUT_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# --- Wichtige Dateien (Beispiele) ---
SCHUELER_MASTER = INPUT_DIR / "schueler_master_liste.json"
KURSE = INPUT_DIR / "kurse.json"
LOGFILE = OUTPUT_DIR / "dashboard_log.txt"

# ----------------------------------------------------------------------
# Zentrale Zugriffsklasse (für Autovervollständigung und Klarheit im Code)
# ----------------------------------------------------------------------
class FilePaths:
    """Enthält alle wichtigen Pfade als Klassenattribute."""

    # Basispfade
    BASE_DIR = BASE_DIR
    SYSTEM_DIR = SYSTEM_DIR
    DATA_DIR = DATA_DIR

    # Konfigurations- und Datenordner
    CONFIG_DIR = CONFIG_DIR
    INPUT_DIR = INPUT_DIR
    OUTPUT_DIR = OUTPUT_DIR

    # Wichtige Dateien
    SCHUELER_MASTER = SCHUELER_MASTER
    KURSE = KURSE
    LOGFILE = LOGFILE

    # Beispiel für eine dynamische Methode (optional)
    @staticmethod
    def get_output_file(filename: str) -> Path:
        """Gibt den Pfad zu einer Datei im OUTPUT-Verzeichnis zurück."""
        return OUTPUT_DIR / filename