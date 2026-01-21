import json
import os
import sys
import hashlib
from datetime import datetime, timezone

# Configuration
REPO_BASE_URL = "https://cci-udes.github.io/Librairie_KiCad_Library"
GITHUB_REPO_URL = "https://github.com/CCI-udes/Librairie_KiCad_Library"

PACKAGES_FILE = "packages.json"
REPO_FILE = "repository.json"

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
    
    zip_sha256 = get_sha256(zip_path)
    zip_size = os.path.getsize(zip_path)
    download_url = f"{GITHUB_REPO_URL}/releases/download/{tag}/{zip_name}"
    
    # Charger packages.json existant
    if os.path.exists(PACKAGES_FILE):
        try:
            with open(PACKAGES_FILE, 'r') as f:
                packages_data = json.load(f)
        except:
            packages_data = {"packages": []}
    else:
        packages_data = {"packages": []}

    if "packages" not in packages_data:
        packages_data["packages"] = []

    # --- DEFINITION DU PAQUET ---
    package_info = {
        "identifier": "com.github.cci-udes.library",
        "name": "C3I KiCad Library",
        "description": "Librairie officielle des composants C3I - UdeS",
        "description_full": "Une collection complète de symboles schématiques, empreintes et modèles 3D validés pour les projets d'ingénierie du C3I.",
        "type": "library",
        "author": {
            "name": "C3I UdeS",
            "contact": {
                "web": GITHUB_REPO_URL
            }
        },
        "license": "CC-BY-SA-4.0",
        "resources": {
            "homepage": GITHUB_REPO_URL
        },
        "versions": []  # <--- CORRECTION ICI : 'versions' au lieu de 'releases'
    }
    
    # Récupérer l'existant
    existing_pkg = next((p for p in packages_data["packages"] if p["identifier"] == "com.github.cci-udes.library"), None)
    if existing_pkg:
        # Si l'ancien fichier utilisait "releases" (vieux format), on le migre, sinon on prend "versions"
        if "versions" in existing_pkg:
            package_info["versions"] = existing_pkg["versions"]
        elif "releases" in existing_pkg:
             package_info["versions"] = existing_pkg["releases"]

    # Création de l'objet Version
    new_version = {
        "version": tag.lstrip('v'),
        "status": "stable",
        "kicad_version": kicad_ver,
        "download_sha256": zip_sha256,
        "download_url": download_url,
        "install_size": zip_size,
        "platforms": ["linux", "windows", "macos"]
    }
    
    # Mise à jour de la liste
    package_info["versions"] = [v for v in package_info["versions"] if v["version"] != new_version["version"]]
    package_info["versions"].insert(0, new_version)
    
    # Sauvegarde dans la liste principale
    packages_data["packages"] = [p for p in packages_data["packages"] if p["identifier"] != "com.github.cci-udes.library"]
    packages_data["packages"].append(package_info)

    with open(PACKAGES_FILE, 'w') as f:
        json.dump(packages_data, f, indent=4)
    
    # --- REPOSITORY.JSON ---
    pkg_sha256 = get_sha256(PACKAGES_FILE)
    now = datetime.now(timezone.utc)
    
    repo_data = {
        "$schema": "https://gitlab.com/kicad/code/kicad/-/raw/master/kicad/pcm/schemas/pcm.v1.schema.json#/definitions/Repository",
        "name": "C3I Repository",
        "maintainer": {
            "name": "C3I UdeS",
            "contact": {
                "web": GITHUB_REPO_URL
            }
        },
        "packages": {
            "url": f"{REPO_BASE_URL}/{PACKAGES_FILE}",
            "sha256": pkg_sha256,
            "update_time_utc": now.strftime("%Y-%m-%d %H:%M:%S"),
            "update_timestamp": int(now.timestamp())
        }
    }

    with open(REPO_FILE, 'w') as f:
        json.dump(repo_data, f, indent=4)

    print(f"Succès v{tag} : Utilisation du champ 'versions'.")

if __name__ == "__main__":
    main()
