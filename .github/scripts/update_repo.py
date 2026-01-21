import json
import os
import sys
import hashlib

# Configuration
REPO_URL = "https://github.com/CCI-udes/Librairie_KiCad_Library"
REPO_JSON_FILE = "repository.json"

def get_sha256(filepath):
    with open(filepath, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def main():
    if len(sys.argv) < 3:
        print("Usage: python update_repo.py <version_tag> <zip_filename> <kicad_version>")
        sys.exit(1)

    tag = sys.argv[1]
    zip_name = sys.argv[2]
    kicad_ver = sys.argv[3]
    zip_path = os.path.join(os.getcwd(), zip_name)
    
    sha256 = get_sha256(zip_path)
    file_size = os.path.getsize(zip_path)
    download_url = f"{REPO_URL}/releases/download/{tag}/{zip_name}"
    
    # --- MODE NETTOYAGE : On repart d'une base saine à chaque fois ---
    # On ignore l'ancien fichier s'il est corrompu pour éviter de traîner les erreurs
    repo_data = {
        "$schema": "https://go.kicad.org/pcm/schemas/v1/repository",
        "name": "C3I Repository",
        "maintainer": {
            "name": "C3I UdeS",
            "contact": {
                "web": REPO_URL
            }
        },
        "packages": []
    }

    # Définition complète du paquet (Strict Standard)
    package = {
        "identifier": "com.github.cci-udes.library",
        "name": "C3I KiCad Library",
        "description": "Librairie officielle des composants C3I - UdeS",
        "license": "CC-BY-SA-4.0",
        "resources": {
            "homepage": REPO_URL
        },
        "releases": []
    }
    
    # On ajoute notre nouvelle release
    new_release = {
        "version": tag.lstrip('v'),
        "status": "stable",
        "kicad_version": kicad_ver,
        "download_sha256": sha256,
        "download_url": download_url,
        "install_size": file_size,
        "platforms": ["linux", "windows", "macos"]
    }
    
    package["releases"].append(new_release)
    repo_data["packages"].append(package)

    with open(REPO_JSON_FILE, 'w') as f:
        json.dump(repo_data, f, indent=4)
    
    print(f"Succès ! Repository régénéré proprement pour la version {tag}.")

if __name__ == "__main__":
    main()
