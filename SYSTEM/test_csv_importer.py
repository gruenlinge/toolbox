#!/usr/bin/env python
# coding: utf-8
"""
test_csv_importer.py – Testet den CSV-Importer.

Erwartet eine Datei 'testdaten.csv' im INPUT-Ordner.
"""

import sys
from pathlib import Path

# Damit wir die Module im SYSTEM-Ordner finden
sys.path.insert(0, str(Path(__file__).parent))
from csv_importer import csv_to_json
from file_manager import FilePaths

def main():
    print("=" * 50)
    print("TEST: CSV-Importer")
    print("=" * 50)

    csv_path = FilePaths.INPUT_DIR / "testdaten.csv"
    json_path = FilePaths.OUTPUT_DIR / "testdaten.json"

    if not csv_path.exists():
        print(f"❌ Bitte lege zuerst eine Test-CSV an: {csv_path}")
        return

    print(f"📄 CSV: {csv_path}")
    print(f"📦 JSON: {json_path}")

    success = csv_to_json(csv_path, json_path, delimiter=';')

    if success:
        print("✅ Test erfolgreich. JSON wurde erstellt.")
    else:
        print("❌ Test fehlgeschlagen.")

if __name__ == "__main__":
    main()