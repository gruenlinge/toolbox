#!/usr/bin/env python
# coding: utf-8
"""
test_config.py – Testet das config_helper-Modul.

Führe es einfach mit `python test_config.py` aus.
"""

from config_helper import Config
from file_manager import FilePaths

def main():
    print("=" * 50)
    print("TEST: config_helper.py")
    print("=" * 50)

    # 1. Standard-Konfiguration laden (Datei wird erstellt, falls nicht vorhanden)
    print("\n1. Lade Standard-Konfiguration...")
    cfg = Config()
    print("   Aktuelle Daten:", cfg.data)

    # 2. Einzelne Werte abfragen
    print("\n2. Einzelne Werte:")
    print(f"   project_name = {cfg.get('project_name')}")
    print(f"   debug        = {cfg.get('debug')}")
    print(f"   nichtvorhanden = {cfg.get('nichtvorhanden', 'Standardwert')}")

    # 3. Wert ändern und speichern
    print("\n3. Ändere project_name in 'Testprojekt'...")
    cfg.set("project_name", "Testprojekt")
    print("   Gespeichert. Neu geladen:")

    cfg2 = Config()
    print(f"   project_name = {cfg2.get('project_name')}")

    # 4. Pfad anzeigen
    print("\n4. Konfigurationsdatei liegt unter:")
    print(f"   {cfg.path}")

    print("\n✅ Alle Tests erfolgreich.")

if __name__ == "__main__":
    main()