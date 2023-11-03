import os
import shutil
from app import db, app  # Zaimportuj obiekt bazy danych i aplikacji z twojej aplikacji

# Funkcja do usuwania ukrytych folderów i plików
def remove_hidden_files_and_folders(directory):
    for root, dirs, files in os.walk(directory):
        for name in files + dirs:
            if name.startswith("."):
                path = os.path.join(root, name)
                if os.path.isfile(path):
                    os.remove(path)
                elif os.path.isdir(path):
                    shutil.rmtree(path)

# Funkcja do sprawdzania pliku konfiguracyjnego SQLAlchemy
def check_sqlalchemy_config():
    # Sprawdź plik konfiguracyjny SQLAlchemy
    from config import SQLALCHEMY_DATABASE_URI  # Zaimportuj konfigurację bazy danych z twojego pliku konfiguracyjnego

    # Przykładowa konfiguracja SQLite (zmień na odpowiednią dla swojego projektu)
    if not SQLALCHEMY_DATABASE_URI.startswith("sqlite:///"):
        print("Nieprawidłowa konfiguracja SQLAlchemy: Należy używać SQLite.")
        # Tutaj można dodać kod do aktualizacji konfiguracji, jeśli to konieczne.

# Funkcja do sprawdzania zmian w kodzie
def check_code_changes():
    # Tutaj można umieścić kod do sprawdzania zmian w modelach bazy danych
    # Porównaj modele z bazą danych i dokonaj aktualizacji, jeśli to konieczne.
    with app.app_context():
        db.create_all()  # Tworzy tabele na podstawie modeli, jeśli nie istnieją

if __name__ == "__main__":
    # Ścieżka do katalogu projektu
    project_directory = "/D:/Python_projekty/BugTracker/app_v2"

    # Usuń ukryte pliki i foldery związane z migracjami
    remove_hidden_files_and_folders(project_directory)

    # Sprawdź plik konfiguracyjny SQLAlchemy
    check_sqlalchemy_config()

    # Sprawdź zmiany w kodzie
    check_code_changes()
