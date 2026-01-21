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
    
    if os.path.exists(REPO_JSON_FILE):
        with open(REPO_JSON_FILE, 'r') as f:
            repo_data = json.load(f)
    else:
        repo_data = {
            "$schema": "https://go.kicad.org/pcm/schemas/v1/repository",
            "packages": []
        }

    # --- CORRECTION V1.0.3 : MAINTAINER EST UN OBJET ---
    repo_data["name"] = "C3I Repository"
    repo_data["maintainer"] = {
        "name": "C3I UdeS",
        "contact": {
            "web": REPO_URL
        }
    }
    # ---------------------------------------------------

    # Trouver ou créer le paquet
    package = next((p for p in repo_data["packages"] if p["identifier"] == "com.github.cci-udes.library"), None)
    if not package:
        package = {
            "identifier": "com.github.cci-udes.library",
            "releases": []
        }
        repo_data["packages"].append(package)

    package["name"] = "C3I KiCad Library"
    package["description"] = "Librairie officielle des composants C3I - UdeS"

    new_release = {
        "version": tag.lstrip('v'),
        "status": "stable",
        "kicad_version": kicad_ver,
        "download_sha256": sha256,
        "download_url": download_url,
        "install_size": file_size,
        "platforms": ["linux", "windows", "macos"]
    }
    
    package["releases"] = [r for r in package["releases"] if r["version"] != new_release["version"]]
    package["releases"].insert(0, new_release)

    with open(REPO_JSON_FILE, 'w') as f:
        json.dump(repo_data, f, indent=4)
    
    print(f"Succès ! Version {tag} corrigée (Maintainer Object).")

if __name__ == "__main__":
    main()
