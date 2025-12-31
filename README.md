# 🌿 Plant Disease Detection System

A web-based application that identifies plant diseases or plant species from leaf images using Deep Learning. Users upload an image of a plant leaf, and the system returns a prediction with confidence scores and suggested remedies.

---

## 🚀 Features

* **Image Upload Interface**
  Simple and intuitive UI for uploading plant leaf images.

* **AI-Powered Analysis**
  Uses a pre-trained Convolutional Neural Network (CNN) for plant disease classification.

* **Real-Time Prediction**
  Fast inference powered by a Flask backend.

* **Responsive UI**
  Clean, user-friendly interface built with HTML, CSS, and JavaScript.

---

## 🛠️ Tech Stack

* **Backend:** Python, Flask
* **Frontend:** HTML5, CSS3, JavaScript
* **Machine Learning:** TensorFlow / Keras or PyTorch
* **Deployment:** Compatible with Heroku, Render, or AWS

---

## 📂 Project Structure

```text
projet_plant/
├── model/              # Pre-trained ML model files (.h5, .pth, .pkl)
├── static/             # CSS, JavaScript, and static assets
├── templates/          # HTML templates (index.html, result.html, etc.)
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
└── .gitattributes      # Git configuration
```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/sunshine13446/projet_plant.git
cd projet_plant
```

### 2. Create a Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate      # Linux / macOS
venv\Scripts\activate         # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python app.py
```

### 5. Access the Web App

Open your browser and navigate to:

```
http://127.0.0.1:5000
```

---

## 🧠 Model Information

* The trained model is stored in the `/model` directory.
* It is trained on plant leaf image datasets such as **PlantVillage**.
* The model is capable of identifying multiple plant diseases and species based on visual patterns in leaf images.

---

## 🤝 Contributing

Contributions are welcome and encouraged.

1. Fork the repository
2. Create a new feature branch

   ```bash
   git checkout -b feature/NewFeature
   ```
3. Commit your changes

   ```bash
   git commit -m "Add NewFeature"
   ```
4. Push to your branch

   ```bash
   git push origin feature/NewFeature
   ```
5. Open a Pull Request

---
