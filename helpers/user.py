from flask import current_app
import boto3
import uuid


s3 = boto3.client('s3')


# Helper to upload file to S3
def upload_to_s3(file, doc_prefix = "profile_pictures", content_type=None, filename=None):
    try:
        # Generate a unique filename
        filename = f"{doc_prefix}/{uuid.uuid4().hex}-{file.filename}" if not filename else f"{doc_prefix}/{uuid.uuid4().hex}-{filename}"
        s3.upload_fileobj(
            file,
            current_app.config['S3_BUCKET'],
            filename,
            ExtraArgs={'ContentType': file.content_type if not content_type else content_type} 
        )
        # Return the public S3 URL
        return f"https://{current_app.config['S3_BUCKET']}.s3.{current_app.config['S3_REGION']}.amazonaws.com/{filename}"
    except Exception as e:
        raise e
