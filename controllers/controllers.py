from helpers.auth import token_required
from services.certificate import analyze_certificate, get_certificate_history
from services.course_recommendation import get_questionnaire_history, predict_course
from services.user import get_profile, signin, signup, update_profile


@token_required
def analyze_certificate_main():
    return analyze_certificate()

@token_required
def predict_course_main():
    return predict_course()

def signin_main():
    return signin()

def signup_main():
    return signup()

@token_required
def user_profile_main():
    return get_profile()

@token_required
def update_profile_main():
    return update_profile()

@token_required
def get_certificate_history_main():
    return get_certificate_history()

@token_required
def get_questionair_history_main():
    return get_questionnaire_history()
