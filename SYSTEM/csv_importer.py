#!/usr/bin/env python
# coding: utf-8
"""
csv_importer.py – Importiert eine CSV-Datei und speichert sie als JSON.

Verwendung:
    python csv_importer.py --input datei.csv --output datei.json [--delimiter ;]

Das Skript nutzt:
    - file_manager für Pfade
    - logger für Ausgaben
    - config_helper für Einstellungen (optional)
    - json_helper für JSON-Export
"""

import argparse
import csv
import sys
from pathlib import Path

# Eigene Module
from file_manager import FilePaths
from logger import Logger
from json_helper import save_json
from config_helper import Config

# Logger initialisieren
log = Logger()

def csv_to_json(csv_path: Path, json_path: Path, delimiter: str = ';') -> bool:
    """
    Liest eine CSV-Datei und speichert die Daten als JSON.

    Args:
        csv_path: Pfad zur CSV-Datei
        json_path: Pfad zur Ausgabe-JSON
        delimiter: Trennzeichen (Standard ';')

    Returns:
        True bei Erfolg, False bei Fehler
    """
    try:
        # CSV lesen
        log.info(f"Lese CSV: {csv_path}")
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=delimiter)
            data = list(reader)
        log.info(f"{len(data)} Zeilen gelesen.")

        # JSON speichern
        save_json(json_path, data)
        log.info(f"JSON gespeichert: {json_path}")
        return True

    except Exception as e:
        log.error(f"Fehler beim Import: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="CSV-zu-JSON-Importer")
    parser.add_argument("--input", help="Name der CSV-Datei im INPUT-Ordner (z.B. daten.csv)")
    parser.add_argument("--output", help="Name der JSON-Datei im OUTPUT-Ordner (optional)")
    parser.add_argument("--delimiter", default=';', help="Feldtrenner (Standard ';')")
    args = parser.parse_args()

    # Wenn keine Argumente, Config fragen (optional)
    cfg = Config()
    default_input = cfg.get("csv_import_default_input", "daten.csv")
    default_output = cfg.get("csv_import_default_output", "daten.json")

    input_file = args.input or default_input
    output_file = args.output or default_output

    # Pfade bauen
    csv_path = FilePaths.INPUT_DIR / input_file
    json_path = FilePaths.OUTPUT_DIR / output_file

    # Prüfen, ob Eingabedatei existiert
    if not csv_path.exists():
        log.error(f"Eingabedatei nicht gefunden: {csv_path}")
        sys.exit(1)

    # Import durchführen
    success = csv_to_json(csv_path, json_path, args.delimiter)

    if success:
        log.info("Import erfolgreich abgeschlossen.")
        sys.exit(0)
    else:
        log.error("Import fehlgeschlagen.")
        sys.exit(1)

if __name__ == "__main__":
    main()