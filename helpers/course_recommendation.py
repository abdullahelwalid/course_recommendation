from tensorflow.keras.models import load_model
import pickle
import os




resultMapper = {
    1: {"name": "Computing And Technology", "Neuroticism": {5: [], 4: [], 3: [], 2: ["Game Development", "Computer Science", "IT", "Software Engineering", "Multimedia Technology", "Cybersecurity", "Artificial Intelligence"], 1: []}, "Agreeableness": {5: [], 4: [], 3: ["Game Development", "Computer Science", "IT", "Software Engineering", "Multimedia Technology", "Artificial Intelligence"], 2: ["Cybersecurity"], 1: []}, "Extraversion": {5: [], 4: [], 3: ["Game Development", "Computer Science", "IT", "Software Engineering", "Multimedia Technology", "Cybersecurity", "Artificial Intelligence"], 2: [], 1: []}, "Conscientiousness": {5: ["Game Development", "Computer Science", "Software Engineering", "IT", "Cybersecurity", "Artificial Intelligence"], 4: ["Multimedia Technology"], 3: [], 2: [], 1: []},"Openness": {5: ["Multimedia Technology", "Game Development", "Artificial Intelligence"], 4: ["Computer Science", "Software Engineering", "IT"], 3: ["Cybersecurity"], 2: [], 1: []}},
    2: {"name": "Art and Design", "Neuroticism": {5: [], 4: [], 3: [], 2: ["Visual Effects", "Animation", "Digital Advertising", "Industrial Design"], 1: []}, "Agreeableness": {5: [], 4: ["Digital Advertisement", "Industrial Design"], 3: ["Visual Effects", "Animation"], 2: [], 1: []}, "Extraversion": {5: ["Digital Advertising"], 4: [], 3: ["Industrial Design"], 2: ["Visual Effects", "Animation"], 1: []}, "Conscientiousness": {5: ["Visual Effects", "Animation", "Industrial Design"], 4: ["Digital Advertising"], 3: [], 2: [], 1: []}, "Openness": {5: ["Visual Effects", "Animation", "Digital Advertising", "Industrial Design"], 4: [], 3: [], 2: [], 1: []}},
    3: {"name": "Business and Marketing", "Neuroticism": {5: [], 4: [], 3: [], 2: ["Business Management", "Marketing Management", "Tourism Management", "International Business Marketing"], 1: ["HR"]}, "Agreeableness": {5: ["HR", "Tourism Management"], 4: ["Marketing Management", "International Business Marketing"], 3: ["Business Management"], 2: [], 1: []}, "Extraversion": {5: ["HR", "Marketing Management", "Tourism Management", "International Business Marketing"], 4: ["Business Management "], 3: [], 2: [], 1: []}, "Conscientiousness": {5: ["Business & Management", "HR", "International Business Marketing"], 4: ["Marketing Management", "Tourism Management"], 3: [], 2: [], 1: []}, "Openness": {5: ["Marketing Management", "Tourism Management", "International Business Marketing"], 4: ["Business & Management", "HR"], 3: [], 2: [], 1: []}},
    4: {"name": "Accounting and Banking", "Neuroticism": {5: [], 4: [], 3: [], 2: [], 1: ["Banking & Finance", "Accounting & Finance", "Actuarial Studies"]}, "Agreeableness": {5: [], 4: [], 3: ["Banking & Finance", "Accounting & Finance", "Actuarial Studies"], 2: [], 1: []}, "Extraversion": {5: [], 4: [], 3: ["Banking & Finance"], 2: ["Accounting & Finance", "Actuarial Studies"], 1: []}, "Conscientiousness": {5: ["Banking & Finance", "Actuarial Studies", "Accounting & Finance"], 4: [], 3: [], 2: [], 1: []}, "Openness": {5: [], 4: ["Banking & Finance"], 3: ["Accounting & Finance", "Actuarial Studies"], 2: [], 1: []}},
    5: {"name": "Engineering", "Neuroticism": {5: [], 4: [], 3: [], 2: [], 1: ["Electrical & Electronic Engineering", "Petroleum Engineering", "Computer Engineering", "Mechatronic Engineering"]}, "Agreeableness": {5: [], 4: [], 3: ["Electrical & Electronic Engineering", "Petroleum Engineering", "Computer Engineering", "Mechatronic Engineering"], 2: [], 1: []}, "Extraversion": {5: [], 4: [], 3: ["Electrical & Electronic  Engineering", "Petroleum Engineering", "Computer Engineering"], 2: ["Mechatronic Engineering"], 1: []}, "Conscientiousness": {5: ["Electrical & Electronic Engineering", "Petroleum Engineering", "Computer Engineering", "Mechatronic Engineering"], 4: [], 3: [], 2: [], 1: []}, "Openness": {5: ["Mechatronic Engineering"], 4: ["Electrical & Electronic Engineering", "Petroleum Engineering", "Computer Engineering"], 3: [], 2: [], 1: []}},
    6: {"name": "Media and Communication", "Neuroticism": {5: [], 4: [], 3: [], 2: ["International Relations", "Media & Communication"], 1: []}, "Agreeableness": {5: [], 4: ["International Relations"], 3: ["Media & Communication"], 2: [], 1: []}, "Extraversion": {5: [], 4: ["International Relations", "Media & Communication"], 3: [], 2: [], 1: []}, "Conscientiousness": {5: ["International Relations"], 4: ["Media & Communication"], 3: [], 2: [], 1: []}, "Openness": {5: ["International Relations", "Media & Communication Studies"], 4: [], 3: [], 2: [], 1: []}},
    7: {"name": "Psychology", "Neuroticism": {5: [], 4: [], 3: ["Psychology"], 2: [], 1: []}, "Agreeableness": {5: ["Psychology"], 4: [], 3: [], 2: [], 1: []}, "Extraversion": {5: [], 4: [], 3: ["Psychology"], 2: [], 1: []}, "Conscientiousness": {5: [], 4: ["Psychology"], 3: [], 2: [], 1: []}, "Openness": {5: ["Psychology"], 4: [], 3: [], 2: [], 1: []}}
}

def get_suggested_courses_with_fallback(predicted_interest, predicted_traits):
    """
    Map the predicted interest and trait scores to suggested courses using resultMapper.
    
    Parameters:
    - predicted_interest: The predicted interest category (integer, 1–7).
    - predicted_traits: A 1D numpy array of predicted trait scores (e.g., [3.5, 2.9, 2.9, 3.0, 2.0]).
    
    Returns:
    - A list of suggested courses based on resultMapper.
    """
    # Initialize suggested courses list
    suggested_courses = []
    interest_name = None

    # Check if the interest exists in resultMapper
    if predicted_interest in resultMapper:
        interest_mapping = resultMapper[predicted_interest]

        interest_name = resultMapper[predicted_interest]["name"]
        
        # Define trait names in order to map traits scores to resultMapper
        trait_names = ["Openness", "Conscientiousness", "Extraversion", "Agreeableness", "Neuroticism"]
        
        # Combine trait names and scores into a list of tuples for sorting
        traits_with_scores = list(zip(trait_names, predicted_traits[0]))
        
        # Sort traits by scores in descending order
        traits_sorted = sorted(traits_with_scores, key=lambda x: x[1], reverse=True)
        
        # Iterate through traits in sorted order
        for trait, score in traits_sorted:
            trait_score = int(score)  # Convert the score to an integer
            
            # Attempt to find courses for the current score
            courses = interest_mapping.get(trait, {}).get(trait_score, [])
            
            # Add courses to the list, avoiding duplicates
            for course in courses:
                if course not in suggested_courses:
                    suggested_courses.append(course)
        
        # Fallback: Attempt to find courses for lower scores
        if not suggested_courses:
            for trait, score in traits_sorted:
                for lower_score in range(int(score) - 1, 0, -1):  # Convert to int and decrement
                    courses = interest_mapping.get(trait, {}).get(lower_score, [])
                    for course in courses:
                        if course not in suggested_courses:
                            suggested_courses.append(course)
        
        # Fallback: Assign default courses if still empty
        if not suggested_courses:
            default_courses = ["General Studies", "Foundational Course"]  # Example fallback courses
            suggested_courses = default_courses

    return suggested_courses, interest_name


def load_model_complete(save_dir, model_name):
    """
    Load the complete model, including the model architecture, weights,
    and the scaler used for preprocessing.
    
    Args:
        save_dir: Directory where the model is saved
        model_name: Name of the model
        
    Returns:
        tuple: (loaded_model, loaded_scaler)
    """
    try:
        # 1. Load the model
        model_path = os.path.join(save_dir, f"{model_name}.keras")
        loaded_model = load_model(model_path)
        print(f"Model loaded from {model_path}")
        
        # 2. Load the scaler
        scaler_path = os.path.join(save_dir, f"{model_name}_scaler.pkl")
        with open(scaler_path, 'rb') as f:
            loaded_scaler = pickle.load(f)
        print(f"Scaler loaded from {scaler_path}")
        
        return loaded_model, loaded_scaler
        
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        return None, None
