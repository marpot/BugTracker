import os
import shutil

# Definiuj przykładową strukturę aplikacji Flask
expected_structure = {
    'app': ['templates', 'static'],
    'migrations': [],
    'tests': [],
    'venv': [],
    'config.py': None,
    'run.py': None,
}

# Ścieżka do katalogu projektu
project_directory = '/ścieżka/do/twojego/projektu'

def diagnose_structure():
    missing_directories = []
    missing_files = []

    for root, dirs, files in os.walk(project_directory):
        relative_path = os.path.relpath(root, project_directory)

        if relative_path not in expected_structure:
            missing_directories.append(relative_path)

        for file in files:
            if file not in expected_structure.get(relative_path, []):
                missing_files.append(os.path.join(relative_path, file))

    return missing_directories, missing_files

def create_missing_structure(missing_directories):
    for directory in missing_directories:
        directory_path = os.path.join(project_directory, directory)
        os.makedirs(directory_path)

def move_files(missing_files):
    for file in missing_files:
        source_path = os.path.join(project_directory, file)
        destination_directory = os.path.dirname(file)
        destination_path = os.path.join(project_directory, destination_directory)

        if not os.path.exists(destination_path):
            os.makedirs(destination_path)

        shutil.move(source_path, destination_path)

if __name__ == "__main__":
    missing_directories, missing_files = diagnose_structure()

    if missing_directories or missing_files:
        print("Brakujące katalogi:")
        for directory in missing_directories:
            print(directory)

        print("\nBrakujące pliki:")
        for file in missing_files:
            print(file)

        create_missing_structure(missing_directories)
        move_files(missing_files)

        print("\nStruktura projektu została zaktualizowana.")
    else:
        print("Struktura projektu jest poprawna.")