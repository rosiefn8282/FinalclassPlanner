from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
from schedule_engine import run_genetic_algorithm  # الگوریتم زمان‌بندی

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './'
app.config['ALLOWED_EXTENSIONS'] = {'xlsx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/schedule', methods=['GET', 'POST'])
def index():
    schedule = None
    if request.method == 'POST':
        if 'file' not in request.files:
            return "فایل ارسال نشد", 400
        file = request.files['file']
        if file.filename == '':
            return "نام فایل نامعتبر است", 400
        if file and allowed_file(file.filename):
            filename = secure_filename("input_data.xlsx")
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            best_schedule, score = run_genetic_algorithm()
            return render_template('index.html', schedule=best_schedule, score=score)
    return render_template('index.html')
    import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    

from output_creator import save_schedule_excel, save_schedule_pdf

# بعد از ساخت زمان‌بندی
best_schedule, score = run_genetic_algorithm()
save_schedule_excel(best_schedule)
save_schedule_pdf(best_schedule)
