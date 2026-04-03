from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
import json
import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')  # from .env

# MongoDB Atlas connection setup
MONGO_URI = os.getenv('MONGO_URI')
DB_NAME = os.getenv('DB_NAME')
COLLECTION_NAME = os.getenv('COLLECTION_NAME')

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/api')
def api():
    data_file = os.path.join(os.path.dirname(__file__), 'data.json')
    try:
        with open(data_file, 'r') as f:
            data = json.load(f)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify(data)

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    error = None
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        if not name or not email:
            error = "Name and Email are required."
        else:
            try:
                collection.insert_one({'name': name, 'email': email})
                return redirect(url_for('success'))
            except Exception as e:
                error = f"Error: {str(e)}"
    return render_template('submit.html', error=error)

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)
