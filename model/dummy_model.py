# model/dummy_model.py
import numpy as np
import random

class DummyModel:
    """Modèle factice pour la démonstration"""
    
    def __init__(self):
        self.classes = [
            "Tomate - Sain",
            "Tomate - Mildiou", 
            "Tomate - Tache bactérienne",
            "Pomme - Tavelure",
            "Pomme - Rouille",
            "Vigne - Black Rot",
            "Vigne - Esca"
        ]
    
    def predict(self, image):
        """Retourne une prédiction aléatoire (pour la démo)"""
        random_class = random.randint(0, len(self.classes)-1)
        confidence = random.uniform(70, 98)
        return self.classes[random_class], confidence