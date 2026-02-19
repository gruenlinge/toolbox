# SYSTEM/test_json.py
from json_helper import load_json, save_json
from file_manager import FilePaths

# 1. Testdaten speichern
test_data = {"name": "Max Mustermann", "alter": 25}
test_path = FilePaths.OUTPUT_DIR / "test.json"
erfolg = save_json(test_path, test_data)
print(f"Speichern erfolgreich? {erfolg}")

# 2. Gespeicherte Daten laden
geladen = load_json(test_path, default={})
print("Geladene Daten:", geladen)

# 3. Test mit nicht vorhandener Datei
nicht_da = load_json(FilePaths.OUTPUT_DIR / "nichtda.json", default={"standard": "wert"})
print("Fallback bei nicht vorhandener Datei:", nicht_da)

# 4. Test mit ungültiger JSON (z.B. Ordnerpfad)
ungueltig = load_json(FilePaths.OUTPUT_DIR, default="Fehler")
print("Fallback bei ungültigem Pfad:", ungueltig)