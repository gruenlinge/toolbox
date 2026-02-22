#!/usr/bin/env python
# coding: utf-8
"""
config_helper.py – Zentrale Konfigurationsverwaltung

Dieses Modul stellt eine Klasse Config bereit, die:
- Eine JSON-Konfigurationsdatei lädt und speichert.
- Fehlende Standardwerte ergänzt.
- Einfachen Lese-/Schreibzugriff über get/set ermöglicht.
- Auf den Basismodulen file_manager (Pfade) und json_helper (JSON-IO) aufbaut.

Verwendung:
    from config_helper import Config
    cfg = Config()  # lädt DATEN/CONFIG/settings.json (Default)
    debug = cfg.get("debug", False)
    cfg.set("project_name", "Mein neues Projekt")
"""

# ----------------------------------------------------------------------
# 1. Importe – wir nutzen unsere bereits etablierten Helfer
# ----------------------------------------------------------------------
from json_helper import load_json, save_json          # Robustes JSON-Handling
from file_manager import FilePaths                     # Zentrale Pfade

# ----------------------------------------------------------------------
# 2. Standard-Konfiguration (kann später erweitert werden)
# ----------------------------------------------------------------------
DEFAULT_CONFIG = {
    "project_name": "Unbenanntes Projekt",   # Name des aktuellen Projekts
    "version": "0.1.0",                       # Versionsnummer (für interne Zwecke)
    "debug": False,                            # Debug-Modus (True/False)
    "last_modified": "",                       # Letzte Änderung (kann automatisch gesetzt werden)
    # Hier können später beliebig viele weitere Einstellungen ergänzt werden
}

# ----------------------------------------------------------------------
# 3. Die Hauptklasse Config
# ----------------------------------------------------------------------
class Config:
    """
    Verwaltet eine JSON-Konfigurationsdatei.

    Attribute:
        path (Path): Pfad zur Konfigurationsdatei.
        data (dict): Die geladenen Konfigurationsdaten.
    """

    def __init__(self, config_path=None):
        """
        Initialisiert die Config-Instanz.

        Args:
            config_path (str|Path, optional): Pfad zur JSON-Konfigurationsdatei.
                Wenn None, wird der Standardpfad verwendet:
                FilePaths.CONFIG_DIR / "settings.json"
        """
        # 1. Pfad festlegen
        if config_path is None:
            # Nutze den zentralen Konfigurationsordner aus file_manager
            self.path = FilePaths.CONFIG_DIR / "settings.json"
        else:
            self.path = FilePaths._ensure_path(config_path)  # Konvertiere zu Path

        # 2. Daten laden (mit Fallback auf DEFAULT_CONFIG)
        self.data = load_json(self.path, default=DEFAULT_CONFIG.copy())

        # 3. Sicherstellen, dass alle Standardwerte vorhanden sind
        self._ensure_defaults()

    # ------------------------------------------------------------------
    def _ensure_defaults(self):
        """
        Ergänzt fehlende Schlüssel aus DEFAULT_CONFIG in self.data
        und speichert die Datei, wenn Änderungen vorgenommen wurden.
        """
        changed = False
        for key, value in DEFAULT_CONFIG.items():
            if key not in self.data:
                self.data[key] = value
                changed = True

        # Wenn wir etwas ergänzt haben, sofort speichern
        if changed:
            self.save()

    # ------------------------------------------------------------------
    def get(self, key, default=None):
        """
        Gibt den Wert eines Konfigurationsschlüssels zurück.

        Args:
            key (str): Der gesuchte Schlüssel.
            default (any): Wert, der zurückgegeben wird, falls der Schlüssel nicht existiert.

        Returns:
            any: Der Wert des Schlüssels oder default.
        """
        return self.data.get(key, default)

    # ------------------------------------------------------------------
    def set(self, key, value):
        """
        Setzt einen Konfigurationswert und speichert die Datei sofort.

        Args:
            key (str): Der zu setzende Schlüssel.
            value (any): Der neue Wert (muss JSON-serialisierbar sein).
        """
        self.data[key] = value
        self.save()

    # ------------------------------------------------------------------
    def save(self):
        """
        Speichert die aktuellen Konfigurationsdaten in die JSON-Datei.
        Nutzt save_json aus dem json_helper.
        """
        save_json(self.path, self.data)

    # ------------------------------------------------------------------
    def __repr__(self):
        """Für die Konsolenausgabe beim Debuggen."""
        return f"Config(path={self.path}, data={self.data})"


# ----------------------------------------------------------------------
# 4. Kleiner Selbsttest, wenn die Datei direkt ausgeführt wird
# ----------------------------------------------------------------------
if __name__ == "__main__":
    print("🧪 Teste config_helper.py ...")

    # Standard-Konfiguration laden (sollte die Datei anlegen, falls sie fehlt)
    cfg = Config()
    print("Geladene Konfiguration:", cfg.data)

    # Wert ändern und speichern
    old = cfg.get("project_name")
    cfg.set("project_name", "Testprojekt (überschrieben)")
    print(f"Projektname geändert von '{old}' auf '{cfg.get('project_name')}'")

    # Nochmal laden (sauberer Test)
    cfg2 = Config()
    print("Neu geladener Wert:", cfg2.get("project_name"))

    print("✅ Test abgeschlossen. Siehe die Datei unter:", cfg.path)