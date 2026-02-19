# SYSTEM/json_helper.py
"""Hilfsfunktionen für das Laden und Speichern von JSON-Dateien."""

import json
from pathlib import Path
from typing import Any, Union

def load_json(path: Union[str, Path], default: Any = None) -> Any:
    """
    Lädt eine JSON-Datei sicher.
    
    Args:
        path: Pfad zur JSON-Datei (String oder Path-Objekt)
        default: Wert, der bei Fehlern zurückgegeben wird (z.B. leeres Dict oder Liste)
    
    Returns:
        Geladene Daten oder default bei Fehler.
    """
    path = Path(path)  # Stelle sicher, dass es ein Path-Objekt ist
    if not path.exists():
        return default
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError, OSError):
        return default

def save_json(path: Union[str, Path], data: Any) -> bool:
    """
    Speichert Daten als JSON-Datei. Erstellt fehlende Ordner automatisch.
    
    Args:
        path: Pfad zur JSON-Datei (String oder Path-Objekt)
        data: Daten, die gespeichert werden sollen (muss JSON-serialisierbar sein)
    
    Returns:
        True bei Erfolg, False bei Fehler.
    """
    path = Path(path)
    try:
        # Elternverzeichnis anlegen, falls nicht vorhanden
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except (IOError, OSError, TypeError):
        return False