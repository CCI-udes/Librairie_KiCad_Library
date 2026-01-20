# Librairie KiCad - C3I

Bienvenue sur le dépôt officiel de la librairie de composants KiCad du **C3I**.
Ce dépôt centralise les symboles, empreintes (footprints) et modèles 3D utilisés dans nos projets de conception électronique.

L'objectif est d'assurer l'uniformité, la réutilisabilité et la fiabilité de nos designs de PCB.

---

## 📂 Structure du Dépôt

L'organisation des fichiers suit la structure standard KiCad :

* `symbols/` : Fichiers `.kicad_sym` (Symboles schématiques)
* `footprints/` : Dossiers `.pretty` contenant les fichiers `.kicad_mod`
* `3dmodels/` : Fichiers `.step` (ou `.wrl`) pour la visualisation 3D

> **Note :** Nous utilisons des chemins relatifs pour les modèles 3D. Assurez-vous que votre variable d'environnement `${C3I_LIB_3D}` (ou équivalent) est correctement configurée dans KiCad si nécessaire, ou utilisez le chemin relatif par défaut `${KIPRJMOD}/3dmodels/...`.

---

## 📏 Normes de Conception (Standards)

Pour garantir la qualité de la librairie, tout ajout doit respecter les normes suivantes. Nous nous basons largement sur la **KiCad Library Convention (KLC)**.

### 1. Conventions de Nommage
* **Langue :** Anglais (Standard industriel).
* **Format :** `Fabricant_NumeroDePiece_Description` (si applicable).
* **Caractères :** Alphanumérique uniquement, pas d'espaces (utiliser `_` ou `-`).
    * *Bon :* `TexasInstruments_LM358_SOIC-8`
    * *Mauvais :* `Ampli op LM358`

### 2. Symboles Schématiques (`.kicad_sym`)
* **Grille :** Les pins doivent toujours être alignées sur une grille de **50 mil (1.27 mm)**.
* **Orientation :**
    * Entrées à gauche, Sorties à droite.
    * Alimentation positive en haut, GND/Négative en bas.
* **Champs obligatoires :**
    * `Reference` (ex: U, R, C)
    * `Value` (Nom de la pièce)
    * `Footprint` (Lien vers l'empreinte correcte dans ce dépôt)
    * `Datasheet` (Lien URL valide vers la fiche technique)

### 3. Empreintes (`.kicad_mod`)
* **Orientation :** Pin 1 toujours en haut à gauche ou selon la norme IPC.
* **Sérigraphie (Silkscreen) :**
    * Doit inclure le contour du composant.
    * Doit clairement indiquer la Pin 1.
    * Le texte ne doit jamais recouvrir un pad.
* **Courtyard (F.CrtYd) :** Obligatoire. Doit définir l'espace physique requis + une marge de sécurité (généralement 0.25mm autour du composant).
* **Pad Stack :** Vérifiez que les tailles de perçage et de cuivre respectent les capacités de notre fabricant de PCB habituel (ex: JLCPCB, PCBWay).

### 4. Modèles 3D
* Format préféré : **STEP** (`.step` ou `.stp`) pour faciliter l'intégration mécanique.
* L'échelle doit être 1:1.
* Le modèle doit être parfaitement aligné avec l'empreinte.

---

## workflow Git & Contribution

Nous utilisons un flux de travail basé sur les **Pull Requests (PR)**. Il est interdit de *commit* directement sur la branche `main` (ou `master`).

### Procédure pour ajouter/modifier un composant :

1.  **Mettez à jour votre dépôt local :**
    ```bash
    git checkout main
    git pull origin main
    ```
2.  **Créez une nouvelle branche** avec un nom descriptif :
    ```bash
    git checkout -b ajout-capteur-imu
    ```
3.  **Faites vos modifications** dans KiCad.
4.  **Vérifiez vos changements (Checklist) :**
    * [ ] Le symbole a-t-il une Datasheet liée ?
    * [ ] Les pins sont-elles sur la grille 50mil ?
    * [ ] L'empreinte a-t-elle été vérifiée avec l'outil de mesure par rapport à la datasheet ?
    * [ ] Le modèle 3D est-il bien calé ?
    * [ ] Avez-vous lancé le "Symbol/Footprint Checker" de KiCad ?
5.  **Commit et Push :**
    ```bash
    git add .
    git commit -m "Add: Bosch BNO055 IMU symbol and footprint"
    git push origin ajout-capteur-imu
    ```
6.  **Ouvrez une Pull Request (PR)** sur GitHub :
    * Décrivez les ajouts.
    * Ajoutez un lien vers la Datasheet dans la description de la PR.
    * Assignez un membre du C3I pour la révision (Review).

---

## ⚠️ Avant de valider une Pull Request (Pour les Reviewers)

Ne fusionnez pas une PR sans avoir vérifié :
1.  **Conformité KLC :** Les normes ci-dessus sont respectées.
2.  **Validité électrique :** Les types de pins (Input, Output, Power Input) sont logiques (pour éviter les erreurs d'ERC futures).
3.  **Faisabilité :** L'empreinte est soudable (pas de pads trop petits ou trop proches pour nos capacités d'assemblage).

---

## 🛠 Installation pour les membres

1. Clonez ce dépôt sur votre machine.
2. Dans KiCad, allez dans **Preferences > Manage Symbol Libraries**.
3. Ajoutez la librairie en mode "Project Specific" ou "Global" selon le besoin.
4. Répétez pour **Manage Footprint Libraries**.
5. Configurez les chemins 3D si nécessaire.

---

*Maintenu par l'équipe électrique du C3I.*
