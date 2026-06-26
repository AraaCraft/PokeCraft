# Utilise une image Python récente et allégée ("slim")
FROM python:3.12-slim

# Définit le dossier de travail à l'intérieur du conteneur
WORKDIR /app

# Copie le fichier des dépendances dans le conteneur
COPY requirements.txt .

# Installe Flask et le reste sans garder le cache pour alléger l'image
RUN pip install --no-cache-dir -r requirements.txt

# Expose le port 5000 (port par défaut de Flask)
EXPOSE 5000

# Commande par défaut pour lancer le serveur Flask
CMD ["flask", "run", "--host=0.0.0.0"]
