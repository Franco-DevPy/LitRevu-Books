\# 📚 LITRevu — Application web Django

LITRevu est une application web développée avec **Django** permettant à une communauté d’utilisateurs de **demander, publier et consulter des critiques de livres ou d’articles**.

Les utilisateurs peuvent créer des tickets pour solliciter des avis, rédiger des critiques, suivre d’autres utilisateurs et consulter un **flux personnalisé** basé sur leurs abonnements.

---

## 🚀 Fonctionnalités principales

- Création de tickets (demande de critique)
- Publication de critiques (reviews)
- Flux personnalisé (feed) :
	- publications de l’utilisateur
	- publications des utilisateurs suivis
- Système d’abonnements (follow / unfollow / block)
- Modification et suppression de ses propres tickets et critiques
- Authentification sécurisée (inscription / connexion / déconnexion)
- Gestion des images associées aux tickets
- Interface respectant les bonnes pratiques d’accessibilité (WCAG)

---

## 🏗️ Architecture du projet

Le projet repose sur l’architecture **MVT (Model – View – Template)** de Django :

- **Models** : structure de la base de données (tickets, critiques, abonnements)
- **Views** : logique métier et traitement des requêtes
- **Templates** : interface utilisateur (HTML, CSS)
- **Forms** : validation et sécurisation des données utilisateur

---

## ⚙️ Prérequis

- Python **3.10+**
- pip
- Virtualenv (recommandé)

---

## 🛠️ Installation et configuration locale

### 1️⃣ Cloner le dépôt

```bash
git clone https://github.com/TON_USERNAME/litrevu.git
cd litrevu
```

### 2️⃣ Créer et activer un environnement virtuel

```bash
python -m venv venv
```

Activation :

- **Windows (PowerShell)** :

```bash
venv\Scripts\Activate.ps1
```

- **Windows (Git Bash)** :

```bash
source venv/Scripts/activate
```

- **macOS / Linux** :

```bash
source venv/bin/activate
```

### 3️⃣ Installer les dépendances

```bash
pip install -r requirements.txt
```

Principales dépendances :

- Django
- Pillow (gestion des images)
- flake8 (PEP8)

### 4️⃣ Appliquer les migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5️⃣ Créer un superutilisateur (optionnel)

```bash
python manage.py createsuperuser
```

### 6️⃣ Lancer le serveur de développement

```bash
python manage.py runserver
```


