import os
import numpy as np
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from PIL import Image
import mysql.connector
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'plant-disease-2025'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

# Extensions autorisées
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Liste des maladies possibles (pour la démo)
DISEASE_DATABASE = {
    "Tomate": ["Sain", "Mildiou", "Tache bactérienne", "Flétrissement", "Oïdium"],
    "Pomme": ["Sain", "Tavelure", "Rouille", "Pourriture"],
    "Vigne": ["Sain", "Black Rot", "Esca", "Mildiou"],
    "Pomme de terre": ["Sain", "Mildiou", "Gale"],
    "Blé": ["Sain", "Rouille", "Charbon"],
    "Autre": ["Sain", "Taches foliaires", "Pourriture racinaire"]
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Connexion à MySQL
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',          # Utilisateur par défaut XAMPP
            password='',          # Mot de passe vide par défaut
            database='plant_disease',
            port=3306
        )
        return connection
    except mysql.connector.Error as err:
        print(f"⚠️ Erreur MySQL: {err}")
        print("⚠️ Vérifie que MySQL est démarré dans XAMPP")
        return None

# Simulation IA (pour la démo)
def predict_with_ai(image_path, plant_type):
    """Simule une prédiction IA"""
    
    # Détermine les maladies possibles pour cette plante
    possible_diseases = DISEASE_DATABASE.get(plant_type, ["Sain", "Malade"])
    
    # Choisis une maladie au hasard
    disease = random.choice(possible_diseases)
    
    # Génère un pourcentage de confiance réaliste
    if disease == "Sain":
        confidence = random.uniform(85.0, 98.0)
    else:
        confidence = random.uniform(75.0, 95.0)
    
    return disease, round(confidence, 2)

# Page d'accueil
@app.route('/')
def index():
    return render_template('index.html')

# Page d'upload
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('Aucun fichier sélectionné')
        return redirect(url_for('index'))
    
    file = request.files['file']
    plant_type = request.form.get('plant_type', 'Inconnu')
    
    if file.filename == '':
        flash('Aucun fichier sélectionné')
        return redirect(url_for('index'))
    
    if file and allowed_file(file.filename):
        # Sauvegarder l'image
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Simulation de l'IA
        disease, confidence = predict_with_ai(file_path, plant_type)
        
        # Sauvegarde dans MySQL
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO predictions (filename, plant_type, disease, confidence) VALUES (%s, %s, %s, %s)",
                    (filename, plant_type, disease, confidence)
                )
                conn.commit()
                cursor.close()
                flash('✅ Analyse sauvegardée avec succès!')
            except mysql.connector.Error as err:
                flash(f'⚠️ Erreur base de données: {err}')
            finally:
                conn.close()
        else:
            flash('⚠️ Impossible de se connecter à la base de données')
        
        # Afficher les résultats
        current_date = datetime.now().strftime('%d/%m/%Y %H:%M')
        
        return render_template('index.html',
                             filename=filename,
                             plant_type=plant_type,
                             disease=disease,
                             confidence=confidence,
                             current_date=current_date,
                             show_results=True)
    
    flash('Type de fichier non supporté')
    return redirect(url_for('index'))

# Page historique
@app.route('/history')
def history():
    conn = get_db_connection()
    predictions = []
    
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM predictions ORDER BY date DESC")
            predictions = cursor.fetchall()
            cursor.close()
        except mysql.connector.Error as err:
            flash(f'Erreur: {err}')
        finally:
            conn.close()
    
    return render_template('history.html', predictions=predictions)

# Supprimer une entrée
@app.route('/delete/<int:id>')
def delete_entry(id):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM predictions WHERE id = %s", (id,))
            conn.commit()
            cursor.close()
            flash('🗑️ Entrée supprimée avec succès')
        except mysql.connector.Error as err:
            flash(f'Erreur: {err}')
        finally:
            conn.close()
    
    return redirect(url_for('history'))

# Page À propos
@app.route('/about')
def about():
    return render_template('about.html')

# Lancer l'application
if __name__ == '__main__':
    # Créer le dossier uploads s'il n'existe pas
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    # Démarrer Flask
    app.run(debug=True, port=5000)