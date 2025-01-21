from helpers.course_recommendation import load_model_complete


class Config(object):
    MODEL_NAME = "personality_model_v2"
    SAVE_DIR = "./modles"
    # Load the .keras model
    LOADED_MODEL, LOADED_SCALAR = load_model_complete(SAVE_DIR, MODEL_NAME)
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
    MAX_CONTENT_LENGTH = 1 * 1000 * 1000
    UPLOAD_FOLDER = './tmp'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///users.db'
    SECRET_KEY = "K#$kjLK269ljk235lSJL@"
    S3_BUCKET = 'textract-console-ap-southeast-1-e5b7ac87-57ba-4401-95b8-86915e7'
    S3_REGION = 'ap-southeast-1'
