import json
import os
import sys
import hashlib
from datetime import datetime, timezone

# Configuration
REPO_BASE_URL = "https://cci-udes.github.io/Librairie_KiCad_Library"
GITHUB_REPO_URL = "https://github.com/CCI-udes/Librairie_KiCad_Library"

# Noms des fichiers générés
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
    
    # 1. Préparer les infos du ZIP
    zip_sha256 = get_sha256(zip_path)
    zip_size = os.path.getsize(zip_path)
    download_url = f"{GITHUB_REPO_URL}/releases/download/{tag}/{zip_name}"
    
    # 2. Créer la structure du PACKAGES.JSON (La liste pure)
    # On essaie de récupérer l'ancienne liste pour ne pas perdre l'historique, 
    # mais si ça plante, on repart à neuf.
    if os.path.exists(PACKAGES_FILE):
        try:
            with open(PACKAGES_FILE, 'r') as f:
                packages_data = json.load(f)
        except:
            packages_data = {"packages": []}
    else:
        packages_data = {"packages": []}

    # On s'assure que la liste existe
    if "packages" not in packages_data:
        packages_data["packages"] = []

    # Définition du paquet (Le contenu C3I)
    package_info = {
        "identifier": "com.github.cci-udes.library",
        "name": "C3I KiCad Library",
        "description": "Librairie officielle des composants C3I - UdeS",
        "license": "CC-BY-SA-4.0",
        "resources": {
            "homepage": GITHUB_REPO_URL
        },
        "releases": []
    }
    
    # Trouver si le paquet existe déjà dans la liste pour le mettre à jour
    existing_pkg = next((p for p in packages_data["packages"] if p["identifier"] == "com.github.cci-udes.library"), None)
    if existing_pkg:
        package_info = existing_pkg # On reprend l'existant

    # Nouvelle release
    new_release = {
        "version": tag.lstrip('v'),
        "status": "stable",
        "kicad_version": kicad_ver,
        "download_sha256": zip_sha256,
        "download_url": download_url,
        "install_size": zip_size,
        "platforms": ["linux", "windows", "macos"]
    }
    
    # Mise à jour de la liste des releases (remplace si version identique)
    package_info["releases"] = [r for r in package_info["releases"] if r["version"] != new_release["version"]]
    package_info["releases"].insert(0, new_release)
    
    # Si c'était un nouveau paquet, on l'ajoute à la liste globale
    if not existing_pkg:
        packages_data["packages"].append(package_info)

    # SAUVEGARDE DE PACKAGES.JSON
    with open(PACKAGES_FILE, 'w') as f:
        json.dump(packages_data, f, indent=4)
    
    print(f"Généré : {PACKAGES_FILE}")

    # 3. Créer le REPOSITORY.JSON (L'enveloppe officielle)
    # C'est ici qu'on applique la structure du JSON officiel que tu as montré
    
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

    # SAUVEGARDE DE REPOSITORY.JSON
    with open(REPO_FILE, 'w') as f:
        json.dump(repo_data, f, indent=4)

    print(f"Généré : {REPO_FILE} (Pointe vers packages.json)")

if __name__ == "__main__":
    main()
