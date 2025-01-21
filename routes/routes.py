from flask import Blueprint, request

from controllers.controllers import analyze_certificate_main, get_certificate_history_main, get_questionair_history_main, predict_course_main, signin_main, signup_main, update_profile_main, user_profile_main


bp = Blueprint("routes", __name__)

@bp.after_request
def set_cors(response):
    origin = request.headers.get('Origin')
    response.headers['Access-Control-Allow-Origin'] = origin
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS, PUT, DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, Accept, Dnt, Sec-Ch-Ua, Sec-Ch-Ua-Mobile, Sec-Ch-Ua-Platform'
    response.headers['Content-Type'] = 'application/json'
    if request.method == 'OPTIONS':
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response


bp.route("/analyze_certificate", methods=["POST"])(analyze_certificate_main)
bp.route("/predict_course", methods=["POST"])(predict_course_main)
bp.route("/certificates/history", methods=["GET"])(get_certificate_history_main)
bp.route("/questionnaires/history", methods=["GET"])(get_questionair_history_main)
bp.route("/signin", methods=["POST"])(signin_main)
bp.route("/signup", methods=["POST"])(signup_main)
bp.route("/profile", methods=["GET"])(user_profile_main)
bp.route("/profile", methods=["PUT"])(update_profile_main)
