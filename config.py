import os

# Ścieżka do katalogu projektu
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Konfiguracja SQLAlchemy
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'bugtracker.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Sekretne klucze
SECRET_KEY = '321meme321'

# Inne ustawienia konfiguracyjne
DEBUG = True  # Ustaw True, aby włączyć tryb debugowania

# Konfiguracja logowania
LOGIN_DISABLED = False

# Inne ustawienia...

# Jeśli masz jakieś dodatkowe ustawienia, możesz je dodać tutaj

