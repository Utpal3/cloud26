from flask import Flask, render_template, request, redirect
import boto3
import sqlite3
from werkzeug.utils import secure_filename

app = Flask(__name__)

# AWS Credentials
AWS_ACCESS_KEY = "YOUR_ACCESS_KEY"
AWS_SECRET_KEY = "YOUR_SECRET_KEY"
BUCKET_NAME = "cloud-storage-project"

s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']

    if file:
        filename = secure_filename(file.filename)

        s3.upload_fileobj(
            file,
            BUCKET_NAME,
            filename
        )

        return "File Uploaded Successfully"

    return "Upload Failed"

@app.route('/files')
def files():
    response = s3.list_objects_v2(
        Bucket=BUCKET_NAME
    )

    file_list = []

    if 'Contents' in response:
        for item in response['Contents']:
            file_list.append(item['Key'])

    return str(file_list)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == "__main__":
    app.run()