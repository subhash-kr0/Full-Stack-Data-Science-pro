from flask import Flask, session, render_template,redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField 

app = Flask(__name__)

class UploadFileForm(FlaskForm):
    file = FileField('file')
    submit = SubmitField('Upload File')

@app.route('/',  methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    form = UploadFileForm()
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)