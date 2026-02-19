# SYSTEM/test_logger.py
from logger import get_logger, info, warning, error
from file_manager import FilePaths

# 1. Logger mit Datei im OUTPUT-Ordner
log = get_logger(log_file=FilePaths.LOGFILE, console=True, min_level="DEBUG")

# 2. Testmeldungen
log.debug("Das ist eine DEBUG-Meldung")
log.info("Info: Skript gestartet")
log.warning("Warnung: Etwas ist seltsam")
log.error("Fehler: Datei nicht gefunden")

# 3. Komfort-Funktionen (nutzen denselben Logger)
info("Diese Info kommt von der Komfort-Funktion")
error("Und das ein Fehler")

print("Logger-Test abgeschlossen. Siehe Logdatei:", FilePaths.LOGFILE)