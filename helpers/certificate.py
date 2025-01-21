from flask import current_app


def parse_igcse_results(lines):
    """
    Parse IGCSE results from Textract output lines into a structured dictionary.
    
    Args:
        lines (list): List of text lines from Textract output
        
    Returns:
        dict: Structured dictionary containing the parsed results
    """
    results = {
        'candidate_info': {},
        'igcse_results': [],
        'gce_results': []
    }
    fields = [[("Candidate Name", "candidate_name",), ("Date of Birth", "dob",), ("Centre / Cand. No.", "center_cand_no",)], [("Centre Name", "center_name",), ("Session", "session",)]]
    #equation = i+|LF|
    for line_fields in fields:
        for field in line_fields:
            for i, line in enumerate(lines):
                if line == field[0]:
                    results['candidate_info'][field[1]] = lines[i + len(line_fields)]
                    print(field[0],":", lines[i + len(line_fields)])
                    break
    # Extract IGCSE and GCE results
    current_section = None
    i = 0
    while i < len(lines):
        if lines[i] == 'IGCSE':
            current_section = 'igcse'
            # Find the next syllabus code
            while i < len(lines) and not (lines[i].strip().isdigit() and len(lines[i].strip()) == 4):
                i += 1
            continue
        elif lines[i] == 'GCE o Level':
            current_section = 'gce'
            # Find the next syllabus code
            while i < len(lines) and not (lines[i].strip().isdigit() and len(lines[i].strip()) == 4):
                i += 1
            continue
            
        # Check if we have a syllabus code (4 digits)
        if i < len(lines) and lines[i].strip().isdigit() and len(lines[i].strip()) == 4:
            if i + 2 < len(lines):
                subject_result = {
                    'syllabus_code': lines[i],
                    'subject_name': lines[i + 1],
                    'grade': lines[i + 2]
                }
                if current_section == 'igcse':
                    results['igcse_results'].append(subject_result)
                elif current_section == 'gce':
                    results['gce_results'].append(subject_result)
                i += 3
            else:
                i += 1
        else:
            i += 1
    return results


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config.get("ALLOWED_EXTENSIONS")
