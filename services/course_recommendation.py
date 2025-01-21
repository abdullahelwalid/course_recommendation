import json
import numpy as np
from flask import jsonify, request, current_app
from app import db

from helpers.course_recommendation import get_suggested_courses_with_fallback
from models.models import QuestionnaireResult

def predict_course():
    loaded_scalar = current_app.config.get("LOADED_SCALAR")
    loaded_model = current_app.config.get("LOADED_MODEL")
    try:
        # Extract input data from query parameters
        questions = [
            float(request.json.get(f"sectionA_Q{i+1}")) for i in range(10)
        ] + [
            float(request.json.get(f"sectionB_Q{i+1}")) for i in range(5)
        ]
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid input. Please provide all 15 question values."}), 400

    # Prepare input for the model
    input_data = np.array(questions).reshape(1, -1)
    print(input_data)

    scaled_input = loaded_scalar.transform(input_data)

    # Predict using the model
    predicted_interest_probs, predicted_traits = loaded_model.predict(scaled_input)

    # Convert interest probabilities to category (0 to 6)
    predicted_interest = np.argmax(predicted_interest_probs) + 1  # Add 1 to map back to the original range (1 to 7)
    print(f"Predicted Interest: {predicted_interest}")

    # Display predicted traits
    print(f"Predicted Traits Scores: {predicted_traits}")

    # Get suggested courses based on the model output
    suggested_courses, interest_name = get_suggested_courses_with_fallback(predicted_interest, predicted_traits)

    # Print suggested courses
    print(f"Suggested Courses: {suggested_courses}")

    results = QuestionnaireResult(
               user_id = request.user_id,
               interest_prediction = interest_name,
               traits_prediction = json.dumps({
                "Openness": float(predicted_traits[0][0]),
                "Conscientiousness": float(predicted_traits[0][1]),
                "Extraversion": float(predicted_traits[0][2]),
                "Agreeableness": float(predicted_traits[0][3]),
                "Neuroticism": float(predicted_traits[0][4])
                }
                ),
               suggested_courses = json.dumps(suggested_courses),
                raw_answers = json.dumps(questions)
            )
    db.session.add(results)
    db.session.commit()

    # Return the results
    return jsonify({
        "interest_prediction": int(predicted_interest),
        "interest_name": interest_name,
        "suggested_courses": suggested_courses,
        "traits_prediction": {
            "Openness": float(predicted_traits[0][0]),
            "Conscientiousness": float(predicted_traits[0][1]),
            "Extraversion": float(predicted_traits[0][2]),
            "Agreeableness": float(predicted_traits[0][3]),
            "Neuroticism": float(predicted_traits[0][4])
        }
    })


def get_questionnaire_history():
    try:
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Query questionnaire results with pagination
        questionnaires = QuestionnaireResult.query.filter_by(
            user_id=request.user_id
        ).order_by(
            QuestionnaireResult.submission_date.desc()
        ).paginate(
            page=page, 
            per_page=per_page,
            error_out=False
        )
        
        # Format the response
        questionnaire_data = [{
            'id': q.id,
            'submission_date': q.submission_date.isoformat(),
            'interest_prediction': q.interest_prediction,
            'traits_prediction': json.loads(q.traits_prediction),
            'suggested_courses': json.loads(q.suggested_courses),
            'raw_answers': json.loads(q.raw_answers)
        } for q in questionnaires.items]
        
        return jsonify({
            'questionnaires': questionnaire_data,
            'total': questionnaires.total,
            'pages': questionnaires.pages,
            'current_page': questionnaires.page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

