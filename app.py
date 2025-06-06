from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename
from schedule_engine import run_genetic_algorithm  # الگوریتم ژنتیک
from output_creator import save_schedule_excel, save_schedule_pdf  # ذخیره خروجی

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './'
app.config['ALLOWED_EXTENSIONS'] = {'xlsx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# مسیر اصلی فرم آپلود
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('file')
        if not file or file.filename == '':
            return "فایل انتخاب نشده یا نامعتبر است.", 400
        if allowed_file(file.filename):
            filename = secure_filename("input_data.xlsx")
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            return render_template('result.html', schedule=best_schedule, score=score)
    return render_template('index.html')

# اجرای سرور
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, port=port, host='0.0.0.0')
