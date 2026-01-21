# Librairie KiCad - C3I

Bienvenue sur le dépôt officiel de la librairie de composants KiCad du **C3I**.
Ce dépôt centralise les symboles, empreintes et modèles 3D validés pour nos projets.

Grâce à l'automatisation mise en place, cette librairie s'installe et se met à jour directement depuis KiCad.

---

## 🚀 Installation (Utilisateurs)

Plus besoin de cloner le dépôt manuellement. Utilisez le **Plugin and Content Manager (PCM)** de KiCad.

1.  Ouvrez **KiCad**.
2.  Cliquez sur l'icône **"Plugin and Content Manager"** (la boîte 📦) dans la fenêtre principale.
3.  Cliquez sur **Gérer les dépôts** (Manage Repositories).
4.  Ajoutez le dépôt du C3I avec ce lien :

    [https://cci-udes.github.io/Librairie_KiCad_Library/repository.json](https://cci-udes.github.io/Librairie_KiCad_Library/repository.json)

5.  Cliquez sur **Enregistrer**.
6.  Dans la liste des extensions, sélectionnez "C3I Repository" dans le menu déroulant (en haut à gauche).
7.  Cliquez sur **Installer** à côté de *C3I KiCad Library*.
8.  Cliquez sur **Appliquer les changements**.

✅ **C'est tout !** Les symboles et empreintes sont maintenant disponibles dans vos projets.
*Quand une mise à jour est disponible, KiCad vous le signalera ici.*

---

## 🤝 Contribuer (Développeurs)

Pour ajouter ou modifier un composant, vous devez passer par Git et GitHub.
**Ne travaillez jamais directement sur `main`.**

### Workflow
1.  **Clonez le dépôt :**
    ```bash
    git clone [https://github.com/CCI-udes/Librairie_KiCad_Library.git](https://github.com/CCI-udes/Librairie_KiCad_Library.git)
    ```
2.  **Créez une branche** pour votre ajout :
    ```bash
    git checkout -b ajout-nouveau-capteur
    ```
3.  **Faites vos modifications** dans KiCad (Éditeurs de symboles/empreintes).
4.  **Sauvegardez** les bibliothèques (`C3I_Library.kicad_sym` et dossier `.pretty`).
5.  **Commit & Push :**
    ```bash
    git add .
    git commit -m "Add: Capteur XYZ"
    git push origin ajout-nouveau-capteur
    ```
6.  **Ouvrez une Pull Request (PR)** sur GitHub pour validation.

---

## 📦 Publication (Administrateurs)

Pour diffuser une mise à jour à tous les membres du C3I via le PCM, il suffit de créer une **Release** sur GitHub. L'automatisation s'occupe du reste.

1.  Assurez-vous que les PR sont mergés dans `main`.
2.  Allez dans la section **Releases** du dépôt GitHub.
3.  Cliquez sur **Draft a new release**.
4.  **Tag version :** Créez un nouveau tag incrémental (ex: `v1.0.9`, `v1.1.0`).
    * *Important : Le tag doit commencer par 'v'.*
5.  Cliquez sur **Publish release**.

🤖 **Le robot va automatiquement :**
* Zipper la librairie.
* Mettre à jour le fichier `repository.json`.
* Rendre la mise à jour visible dans le PCM de tout le monde sous quelques minutes.

---

## 📏 Normes de Conception (Standards)

Pour garantir la qualité de la librairie :

### 1. Symboles (`.kicad_sym`)
* **Grille :** Les pins doivent être alignées sur la grille de **50 mil (1.27 mm)**.
* **Orientation :** Entrées à gauche, Sorties à droite, Alim en haut, GND en bas.
* **Champs :** Remplir `Datasheet` et `Footprint`.

### 2. Empreintes (`.kicad_mod`)
* **Pin 1 :** Toujours clairement identifiée.
* **Courtyard :** Contour de sécurité obligatoire (`F.CrtYd`).
* **3D :** Utiliser des chemins relatifs pour les modèles 3D.

---
*Maintenu par l'équipe électrique du C3I.*
