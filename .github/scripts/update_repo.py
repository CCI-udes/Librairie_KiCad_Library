import json
import os
import sys
import hashlib
from datetime import datetime

# Configuration
REPO_URL = "https://github.com/CCI-udes/Librairie_KiCad_Library"
METADATA_FILE = "metadata.json"
REPO_JSON_FILE = "repository.json"

def get_sha256(filepath):
    with open(filepath, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def main():
    if len(sys.argv) < 3:
        print("Usage: python update_repo.py <version_tag> <zip_filename> <kicad_version>")
        sys.exit(1)

    tag = sys.argv[1] # ex: v1.0.0
    zip_name = sys.argv[2] # ex: C3I-Lib-v1.0.0.zip
    kicad_ver = sys.argv[3] # ex: 7.0
    zip_path = os.path.join(os.getcwd(), zip_name)
    
    # 1. Calcul du SHA256
    sha256 = get_sha256(zip_path)
    file_size = os.path.getsize(zip_path)
    download_url = f"{REPO_URL}/releases/download/{tag}/{zip_name}"
    
    # 2. Lire le repository.json existant ou en créer un
    if os.path.exists(REPO_JSON_FILE):
        with open(REPO_JSON_FILE, 'r') as f:
            repo_data = json.load(f)
    else:
        repo_data = {
            "$schema": "https://go.kicad.org/pcm/schemas/v1/repository",
            "packages": []
        }

    # 3. Trouver ou créer l'entrée du paquet
    package = next((p for p in repo_data["packages"] if p["identifier"] == "com.github.cci-udes.library"), None)
    if not package:
        package = {"identifier": "com.github.cci-udes.library", "releases": []}
        repo_data["packages"].append(package)

    # 4. Ajouter la nouvelle release en haut de la liste
    new_release = {
        "version": tag.lstrip('v'), # Enleve le 'v' si présent
        "status": "stable",
        "kicad_version": kicad_ver,
        "download_sha256": sha256,
        "download_url": download_url,
        "install_size": file_size,
        "platforms": ["linux", "windows", "macos"] # Support universel pour les libs
    }
    
    # Supprime la version si elle existe déjà pour la remplacer
    package["releases"] = [r for r in package["releases"] if r["version"] != new_release["version"]]
    package["releases"].insert(0, new_release)

    # 5. Sauvegarder
    with open(REPO_JSON_FILE, 'w') as f:
        json.dump(repo_data, f, indent=4)
    
    print(f"Succès ! Ajout de la version {tag} au repository.json")

if __name__ == "__main__":
    main()
