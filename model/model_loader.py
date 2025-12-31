# model/model_loader.py
import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np

def create_simple_model():
    """Crée un modèle CNN simple pour la classification"""
    model = models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)),
        layers.MaxPooling2D((2, 2)),
        
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        
        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        
        layers.Flatten(),
        layers.Dense(512, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(3, activation='softmax')  # 3 classes
    ])
    
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

# Classes de maladies (simplifiées pour la démo)
CLASS_NAMES = [
    "Tomate - Sain",
    "Tomate - Mildiou",
    "Tomate - Tache bactérienne"
]

def predict_disease(image_array, model):
    """Fait une prédiction sur une image"""
    # Redimensionner
    img = tf.image.resize(image_array, (150, 150))
    
    # Normaliser
    img = img / 255.0
    
    # Ajouter dimension batch
    img = np.expand_dims(img, axis=0)
    
    # Prédiction
    predictions = model.predict(img, verbose=0)
    predicted_class = np.argmax(predictions[0])
    confidence = float(predictions[0][predicted_class]) * 100
    
    return CLASS_NAMES[predicted_class], confidence