# course_recommendation
# AI-Powered Course Recommendation System

## Introduction

This system is an AI-powered course recommendation platform designed to assist students in selecting a university course based on their personality traits and interests. The system leverages psychological and interest-based questions to analyze a student's responses and predict suitable courses using a trained machine learning model.

The backend is built using **Flask** and serves as the core API for processing user inputs, loading the trained model, and returning predictions. The system's architecture includes structured data handling, model training, and endpoint-based API interactions.

## Features
- **Personality & Interest-Based Analysis**: Uses a structured questionnaire to assess students.
- **AI Model Prediction**: Employs a trained machine learning model to recommend courses.
- **Flask API**: Provides endpoints for receiving responses and returning predictions.
- **Data Preprocessing & Model Training**: Includes a pipeline for cleaning data and training the model.
- **Scalable & Modular Design**: Follows a structured architecture for maintainability.

## Folder Structure
```
.github/workflows      # GitHub Actions for CI/CD
controllers/          # API controllers handling request logic
data/                # Stores dataset files
helpers/             # Utility functions and helper modules
instance/            # Configuration and environment files
migrations/          # Database migrations (if applicable)
models/              # Contains the trained AI models
modles/              # (Typo or duplicate folder, should be models)
routes/              # API route definitions
services/            # Business logic and services
.gitignore           # Files to be ignored in version control
LICENSE              # License details
README.md            # Project documentation
app.py               # Main application entry point
config.py            # Configuration settings
requirements.txt     # Python dependencies
```

## Technical Documentation

### Setup & Installation

1. **Clone the Repository**
   ```sh
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Create a Virtual Environment (Recommended)**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```

4. **Run the Flask API**
   ```sh
   python app.py
   ```

### API Endpoints

#### 1. **Submit Responses & Get Course Prediction**
- **Endpoint:** `POST /predict`
- **Description:** Accepts a JSON payload of answers and returns recommended courses.
- **Request Example:**
  ```json
  {
    "responses": ["a", "b", "c", "d", "e"]
  }
  ```
- **Response Example:**
  ```json
  {
    "recommended_courses": ["Computer Science", "Psychology"]
  }
  ```

#### 2. **Get List of Questions**
- **Endpoint:** `GET /questions`
- **Description:** Returns all personality and interest-based questions.
- **Response Example:**
  ```json
  {
    "questions": [
      {
        "id": 1,
        "question": "How excited are you to travel to a new country?",
        "options": [
          "Not at all excited",
          "Slightly excited",
          "Neutral",
          "Quite excited",
          "Extremely excited"
        ]
      }
    ]
  }
  ```

### Model Training & Data Handling
- **`dataGeneration.ipynb`**: Handles data cleaning, feature engineering, and model training.
- **Model Storage**: Trained models are stored in the `models/` directory and loaded by the API.

### Future Improvements
- Improve model accuracy with more training data.
- Expand course recommendations to cover more domains.
- Implement user authentication for personalized tracking.

---
### License
This project is open-source and licensed under [MIT License](LICENSE).

