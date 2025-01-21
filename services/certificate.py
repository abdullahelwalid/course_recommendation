import json
import os
from werkzeug.utils import secure_filename
import boto3
from flask import current_app, jsonify, request
from helpers.certificate import allowed_file, parse_igcse_results
from helpers.user import upload_to_s3
from models.models import Certificate, QuestionnaireResult
from app import db


def analyze_certificate():
    if 'file' not in request.files:
        return jsonify({"error": "file not in request"}), 400
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        return jsonify({"error": "filename is not valid"})
    if not file or not allowed_file(file.filename):
        return jsonify({"error": "file is not supported"}), 400
    filename = secure_filename(file.filename)

    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

    try:
        client = boto3.client('textract')
        with open(f"./tmp/{filename}", "rb") as b:
            res_text = client.detect_document_text(
                        Document={
                            'Bytes': b.read()
                    }
                )
        with open(f"./tmp/{filename}", "rb") as b:    
            certificate_url = upload_to_s3(b, "certificates", file.content_type, filename)

        lines = []
        for item in res_text['Blocks']:
            if item['BlockType'] == 'LINE':
                #print(item['Text'])
                lines.append(item['Text'])
        results = parse_igcse_results(lines)
        os.remove(f"./tmp/{filename}")
        results_log = Certificate(
                    user_id = request.user_id,
                    title = "O LEVEL IGCSE Certificate",
                    issuing_school = results['candidate_info'].get('center_name'),
                    certificate_url = certificate_url if certificate_url else None
                )
        db.session.add(results_log)
        db.session.commit()
        return jsonify(results), 200
    except Exception as e:
        print(e)
        os.remove(f"./tmp/{filename}")
        return jsonify({"error": "An error has occurred"}), 500

def get_certificate_history():
    try:
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Query certificates with pagination
        certificates = Certificate.query.filter_by(
            user_id=request.user_id
        ).order_by(
            Certificate.created_at.desc()
        ).paginate(
            page=page, 
            per_page=per_page,
            error_out=False
        )
        
        # Format the response
        certificates_data = [{
            'id': cert.id,
            'title': cert.title,
            'issuing_school': cert.issuing_school,
            'certificate_url': cert.certificate_url,
            'created_at': cert.created_at.isoformat()
        } for cert in certificates.items]
        
        return jsonify({
            'certificates': certificates_data,
            'total': certificates.total,
            'pages': certificates.pages,
            'current_page': certificates.page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
