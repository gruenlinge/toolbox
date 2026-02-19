# SYSTEM/test_paths.py
from file_manager import FilePaths

print("BASE_DIR:", FilePaths.BASE_DIR)
print("CONFIG_DIR:", FilePaths.CONFIG_DIR)
print("SCHUELER_MASTER:", FilePaths.SCHUELER_MASTER)

# Prüfen, ob der Beispiel-Pfad existiert (muss nicht, reicht zur Demonstration)
print("Logfile sollte in:", FilePaths.LOGFILE)