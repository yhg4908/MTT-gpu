import os
from flask import Flask, request, send_file, render_template, redirect
from werkzeug.utils import secure_filename
from utils.arranger import AIPianoArranger

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process-file', methods=['POST'])
def process_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    filename = secure_filename(file.filename)
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(input_path)
    base_output = os.path.join(app.config['UPLOAD_FOLDER'], os.path.splitext(filename)[0])
    arranger = AIPianoArranger()
    try:
        midi_file = arranger.process(input_path, base_output)
        return send_file(midi_file, as_attachment=True)
    except Exception as e:
        return f"악보 생성 실패: {e}", 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
